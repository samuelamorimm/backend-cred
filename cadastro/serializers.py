from rest_framework import serializers
from datetime import date
from validate_docbr import CPF, CNPJ
from .models import *

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'


class PessoaFisicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaFisica
        fields = '__all__'

    def validate_cpf(self, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise serializers.ValidationError("CPF inválido")
        return value

    def validate_data_nascimento(self, value):
        if value > date.today():
            raise serializers.ValidationError('A data de nascimento não pode ser no futuro.')
        return value



class PessoaJuridicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaJuridica
        fields = '__all__'


class VinculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vinculo
        fields = '__all__'


class PedidoCredencialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoCredencial
        fields = '__all__'


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


class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'
