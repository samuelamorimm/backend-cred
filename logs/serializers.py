from rest_framework import serializers
from .models import LogDeAcesso

class LogDeAcessoSerializer(serializers.ModelSerializer):
  class Meta:
    model = LogDeAcesso
    fields = ['id', 'user', 'acao', 'resultado', 'detalhes']
    
