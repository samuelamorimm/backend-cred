
from rest_framework import serializers
from cadastro.models import Observacao, EvolucaoPedido, PedidoCredencial
from .models import LogDeAcesso

class LogDeAcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogDeAcesso
        fields = ['id', 'user', 'acao', 'resultado', 'detalhes']


class ObservacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observacao
        fields = ['id', 'titulo', 'conteudo', 'user_id', 'pedido_credencial']
        read_only_fields = ['id', 'user_id']

    def create(self, validated_data):
        # Adiciona o user_id do request ao criar
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)

class EvolucaoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvolucaoPedido
        fields = ['id', 'status_evolucao', 'pedido_credencial', 'user_id']
        read_only_fields = ['id', 'user_id']

    def create(self, validated_data):
        # Adiciona o user_id do request ao criar
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data) 