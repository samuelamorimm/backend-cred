from rest_framework import routers
from django.urls import path, include
from .views import (
    EstadoViewSet, MunicipioViewSet, PessoaFisicaViewSet, PessoaJuridicaViewSet,
    VinculoViewSet, PedidoCredencialViewSet, EvolucaoPedidoViewSet,
    ObservacaoViewSet, DocumentoViewSet
)

router = routers.DefaultRouter()
router.register(r'estados', EstadoViewSet)
router.register(r'municipios', MunicipioViewSet)
router.register(r'pessoas-fisicas', PessoaFisicaViewSet)
router.register(r'pessoas-juridicas', PessoaJuridicaViewSet)
router.register(r'vinculos', VinculoViewSet)
router.register(r'pedidos-credencial', PedidoCredencialViewSet)
router.register(r'evolucoes-pedido', EvolucaoPedidoViewSet)
router.register(r'observacoes', ObservacaoViewSet)
router.register(r'documentos', DocumentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
