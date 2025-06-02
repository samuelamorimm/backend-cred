from rest_framework import serializers
from app.models import Estado, Municipio, PessoaFisica, PessoaJuridica, Vinculo, PedidoCredencial, EvolucaoPedido, Observacao, Documento

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


class EvolucaoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvolucaoPedido
        fields = '__all__'


class ObservacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observacao
        fields = '__all__'


class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'
