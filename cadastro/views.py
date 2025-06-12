from django.shortcuts import render

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from .models import PedidoCredencial
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class EstadoViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAdminUser]
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class MunicipioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class PessoaFisicaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaFisicaSerializer
    http_method_names = ['post']

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

#-----------------filtro em pessoa fisica------------------    
class PessoaFisicaFiltro(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaFisicaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cpf', 'nome', 'sexo', 'estado_civil', 'municipio', 'estado']
#-----------------filtro em pessoa fisica------------------ 


class PessoaJuridicaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PessoaJuridica.objects.all()
    serializer_class = PessoaJuridicaSerializer
    http_method_names = ['get', 'post']

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
#-----------------filtro em pessoa Juridica------------------    
class PessoaJuridicaFiltro(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = PessoaJuridica.objects.all()
    serializer_class = PessoaJuridicaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cnpj', 'razao_social', 'municipio', 'estado']
#-----------------filtro em pessoa Juridica------------------ 

class VinculoViewSet(viewsets.ModelViewSet):
    queryset = Vinculo.objects.all()
    serializer_class = VinculoSerializer

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class PedidoCredencialViewSet(viewsets.ModelViewSet):
    queryset = PedidoCredencial.objects.all()
    serializer_class = PedidoCredencialSerializer


    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

def export_pedidos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Data Pedido', 'Status', 'Nome Pessoa', 'Empresa'])

    pedidos = PedidoCredencial.objects.select_related('vinculo__pessoafisica', 'vinculo__pessoajuridica').all()

    for pedido in pedidos:
        writer.writerow([
            pedido.id,
            pedido.data_pedido.strftime('%d/%m/%Y %H:%M'),
            pedido.status_pedido,
            pedido.vinculo.pessoafisica.nome if pedido.vinculo.pessoafisica else '',
            pedido.vinculo.pessoajuridica.razao_social if pedido.vinculo.pessoajuridica else ''
        ])

    return response

def export_pedidos_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedidos.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "Relatório de Pedidos")
    y -= 40

    p.setFont("Helvetica", 10)
    pedidos = PedidoCredencial.objects.select_related('vinculo__pessoafisica', 'vinculo__pessoajuridica').all()

    for pedido in pedidos:
        texto = (
            f"ID: {pedido.id} | Data: {pedido.data_pedido.strftime('%d/%m/%Y %H:%M')} "
            f"| Status: {pedido.status_pedido} | "
            f"Pessoa: {pedido.vinculo.pessoafisica.nome if pedido.vinculo.pessoafisica else ''} | "
            f"Empresa: {pedido.vinculo.pessoajuridica.razao_social if pedido.vinculo.pessoajuridica else ''}"
        )
        p.drawString(50, y, texto)
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    return response