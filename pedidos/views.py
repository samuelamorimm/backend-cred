from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from cadastro.models import PedidoCredencial, Vinculo, PessoaFisica, Documento
from cadastro.serializers import PedidoCredencialSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class ConsultaPedido(APIView):
  permission_classes = [IsAuthenticated]

  @swagger_auto_schema(
        operation_description="Consulta o pedido de credencial de uma pessoa usando CPF e data de nascimento.",
        manual_parameters=[
            openapi.Parameter(
                'cpf',
                in_=openapi.IN_QUERY,
                description="CPF da pessoa (somente números)",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'data',
                in_=openapi.IN_QUERY,
                description="Data de nascimento no formato YYYY-MM-DD",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(description="Pedido encontrado com sucesso."),
            400: "CPF e data de nascimento são obrigatórios.",
            404: "Pessoa ou pedido não encontrado."
        }
    )
  
  

  def get(self, request):
    data_nascimento = request.query_params.get('data')
    cpf = request.query_params.get('cpf')

    if not cpf or not data_nascimento:
      return Response({
        "erro": "CPF e data de nascimento são obrigatórios."
      })
    
    try:
      pessoa = PessoaFisica.objects.get(cpf=cpf, data_nascimento=data_nascimento)
    except PessoaFisica.DoesNotExist:
      return Response({
        "erro": "Pessoa não encontrada com os dados fornecidos.",
      }, status=status.HTTP_404_NOT_FOUND)
  
    pedido = PedidoCredencial.objects.filter(vinculo__pessoafisica=pessoa).first()

    if not pedido:
      return Response({
        "erro": "Nenhum pedido de credencial encontrado para esta pessoa."
      }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PedidoCredencialSerializer(pedido)
    return Response(serializer.data, status=status.HTTP_200_OK)


    
class UploadDocumento(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [MultiPartParser]


  @swagger_auto_schema(
        operation_description="Upload de documento para um pedido de credencial.",
        manual_parameters=[
            openapi.Parameter('pedido_credencial', openapi.IN_FORM, type=openapi.TYPE_INTEGER, required=True, description='ID do pedido'),
            openapi.Parameter('tipo_documento', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description='Tipo do documento'),
            openapi.Parameter('nome_documento', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False, description='Nome do documento'),
            openapi.Parameter('arquivo', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True, description='Arquivo a ser enviado'),
        ],
        responses={
            201: openapi.Response('Documento criado com sucesso'),
            400: 'Erro de validação',
            404: 'Pedido não encontrado',
        }
    )


  def post(self, request):
    pedido_id = request.data.get('pedido_credencial')
    tipo_documento = request.data.get('tipo_documento')
    nome_documento = request.data.get('nome_documento')
    arquivo = request.FILES.get('arquivo')

    if not (pedido_id and arquivo):
      return Response({
        "erro": "Campos obrigatórios faltando."
      }, status=status.HTTP_400_BAD_REQUEST)  

    try:
      pedido = PedidoCredencial.objects.get(id=pedido_id)
    except PedidoCredencial.DoesNotExist:
      return Response({
        'erro': 'Pedido não encontrado'
      }, status=status.HTTP_404_NOT_FOUND)
    
    doc = Documento.objects.create(
      nome_documento=nome_documento or arquivo.name,
      tipo_documento=tipo_documento,
      arquivo=arquivo,
      pedido_credencial=pedido
    )

    return Response({
      'id': doc.id,
      'arquivo_url': doc.arquivo.url,
    }, status=status.HTTP_201_CREATED)