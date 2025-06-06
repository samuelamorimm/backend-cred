from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObservacaoViewSet, EvolucaoPedidoViewSet

router = DefaultRouter()
router.register(r'observacoes', ObservacaoViewSet)
router.register(r'evolucoes', EvolucaoPedidoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('users.urls')),
    path('', include(router.urls)),
]
