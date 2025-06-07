from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import LogDeAcesso
from .serializers import LogDeAcessoSerializer
from rest_framework.permissions import IsAdminUser
# Create your views here.

class LogDeAcessoViewSet(ModelViewSet):
  permission_classes = [IsAdminUser]
  queryset = LogDeAcesso.objects.all()
  serializer_class = LogDeAcessoSerializer
