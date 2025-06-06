
from django.urls import path, include
from .views import ConsultaPedido, UploadDocumento

urlpatterns = [
    path('consulta/', ConsultaPedido.as_view(), name='consulta'), #api/consulta/?cpf=10000000000&data=12-10-2025
    path('upload/', UploadDocumento.as_view(), name='upload-documento')
]
