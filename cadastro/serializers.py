from rest_framework import serializers
from app.models import (
    Estado, Municipio, PessoaFisica, PessoaJuridica,
    Vinculo, PedidoCredencial, EvolucaoPedido, Observacao, Documento
)
from .validators import (
    validar_cep, validar_telefone, validar_email_personalizado,
    validar_datas_nascimento_emissao, validar_cpf, validar_cnpj,
    validar_status_pedido, validar_renda
)


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

    def validate_cep(self, value):
        validar_cep(value)
        return value

    def validate_fone_celular(self, value):
        validar_telefone(value)
        return value

    def validate_fone_residencial(self, value):
        validar_telefone(value)
        return value

    def validate_email(self, value):
        validar_email_personalizado(value)
        return value

    def validate_cpf(self, value):
        validar_cpf(value)
        return value

    def validate(self, data):
        data_nascimento = data.get('data_nascimento')
        data_emissao = data.get('data_emissao')
        if data_nascimento:
            validar_datas_nascimento_emissao(data_nascimento, data_emissao)
        return data


class PessoaJuridicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaJuridica
        fields = '__all__'

    def validate_cep(self, value):
        validar_cep(value)
        return value

    def validate_fone(self, value):
        validar_telefone(value)
        return value

    def validate_email(self, value):
        validar_email_personalizado(value)
        return value

    def validate_cnpj(self, value):
        validar_cnpj(value)
        return value


class VinculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vinculo
        fields = '__all__'

    def validate_renda(self, value):
        validar_renda(value)
        return value


class PedidoCredencialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoCredencial
        fields = '__all__'

    def validate_status_pedido(self, value):
        validar_status_pedido(value)
        return value


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
