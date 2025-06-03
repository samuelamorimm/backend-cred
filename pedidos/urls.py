
from django.urls import path, include
from .views import ConsultaPedido

urlpatterns = [
    path('api/consulta/', ConsultaPedido.as_view(), name='consulta'), #api/consulta/?cpf=10000000000&data=12-10-2025
]
