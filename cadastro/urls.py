from rest_framework import routers
from django.urls import path, include
from .views import *
from statusPedido.views import AtualizarStatusPedidoView

router = routers.DefaultRouter()
router.register(r'estados', EstadoViewSet)
router.register(r'municipios', MunicipioViewSet)
router.register(r'pessoas-fisicas', PessoaFisicaViewSet)
router.register(r'pessoas-juridicas', PessoaJuridicaViewSet)
router.register(r'vinculos', VinculoViewSet)
router.register(r'pedidos-credencial', PedidoCredencialViewSet)
router.register(r'evolucoes', EvolucaoPedidoViewSet)
router.register(r'observacoes', ObservacaoViewSet)
router.register(r'documentos', DocumentoViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('pedido/<int:pedido_id>/atualizar-status/', AtualizarStatusPedidoView.as_view()),
    path('exportar/pedidos.csv', export_pedidos_csv, name='exportar_pedidos_csv'),
    path('exportar/pedidos.pdf', export_pedidos_pdf, name='exportar_pedidos_pdf'),
]
