from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import LogDeAcesso
from .serializers import LogDeAcessoSerializer
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class LogDeAcessoViewSet(ModelViewSet):
  permission_classes = [IsAdminUser]
  queryset = LogDeAcesso.objects.all()
  serializer_class = LogDeAcessoSerializer

  @swagger_auto_schema(auto_schema=None)
  def destroy(self, request, *args, **kwargs):
    return super().destroy(request, *args, **kwargs)