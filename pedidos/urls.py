
from django.urls import path, include
from .views import ConsultaPedido

urlpatterns = [
    path('api/consulta/', ConsultaPedido.as_view(), name='consulta'),
]
