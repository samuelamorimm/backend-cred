from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import LogDeAcesso
from .serializers import LogDeAcessoSerializer
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from cadastro.models import Observacao, EvolucaoPedido, PedidoCredencial
from logs.serializers import ObservacaoSerializer, EvolucaoPedidoSerializer
# Create your views here.

class LogDeAcessoViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = LogDeAcesso.objects.all()
    serializer_class = LogDeAcessoSerializer

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# Create your views here.

class ObservacaoViewSet(viewsets.ModelViewSet):
    queryset = Observacao.objects.all()
    serializer_class = ObservacaoSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Observacao.objects.all()
        pedido_id = self.request.query_params.get('pedido_id', None)
        if pedido_id is not None:
            queryset = queryset.filter(pedido_credencial_id=pedido_id)
        return queryset

class EvolucaoPedidoViewSet(viewsets.ModelViewSet):
    queryset = EvolucaoPedido.objects.all()
    serializer_class = EvolucaoPedidoSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = EvolucaoPedido.objects.all()
        pedido_id = self.request.query_params.get('pedido_id', None)
        if pedido_id is not None:
            queryset = queryset.filter(pedido_credencial_id=pedido_id)
        return queryset

    @action(detail=False, methods=['get'])
    def ultima_evolucao(self, request):
        pedido_id = request.query_params.get('pedido_id')
        if not pedido_id:
            return Response({"error": "pedido_id é obrigatório"}, status=400)
        
        ultima_evolucao = EvolucaoPedido.objects.filter(
            pedido_credencial_id=pedido_id
        ).order_by('-id').first()
        
        if not ultima_evolucao:
            return Response({"error": "Nenhuma evolução encontrada"}, status=404)
        
        serializer = self.get_serializer(ultima_evolucao)
        return Response(serializer.data)