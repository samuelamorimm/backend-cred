from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from .views import *

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
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include(router.urls)),
]
