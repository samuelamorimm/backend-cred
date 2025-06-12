import re
import phonenumbers
from rest_framework import serializers
from datetime import date
from validate_docbr import CPF, CNPJ
from .models import *

# ======= Funções utilitárias =======
def validar_cep(value):
    cep = re.sub(r'\D', '', value)
    if len(cep) != 8:
        raise serializers.ValidationError("CEP deve conter 8 dígitos numéricos")
    return f"{cep[:5]}-{cep[5:]}"  # Formato: 00000-000

def validar_telefone(value):
    if not value:
        return value
    try:
        number = phonenumbers.parse(value, "BR")
        if not phonenumbers.is_valid_number(number):
            raise serializers.ValidationError("Número de telefone inválido")
        return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL)
    except phonenumbers.NumberParseException:
        raise serializers.ValidationError("Número de telefone inválido")

def validar_numero(value):
    if not value:
        raise serializers.ValidationError("Número é obrigatório")
    return value

# ======= Serializers principais =======
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

    def validate_fone_celular(self, value):
        return validar_telefone(value)

    def validate_fone_residencial(self, value):
        return validar_telefone(value)

    def validate_fone(self, value):
        return validar_telefone(value)

    def validate_cpf(self, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise serializers.ValidationError("CPF inválido")
        return cpf.mask(value)

    def validate_data_nascimento(self, value):
        if value > date.today():
            raise serializers.ValidationError("A data de nascimento não pode ser no futuro.")
        return value

    def validate_cep(self, value):
        return validar_cep(value)

    def validate_numero(self, value):
        return validar_numero(value)

class PessoaJuridicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaJuridica
        fields = '__all__'

    def validate_fone_celular(self, value):
        return validar_telefone(value)

    def validate_fone_residencial(self, value):
        return validar_telefone(value)

    def validate_fone(self, value):
        return validar_telefone(value)

    def validate_cnpj(self, value):
        cnpj = CNPJ()
        if not cnpj.validate(value):
            raise serializers.ValidationError("CNPJ inválido")
        return cnpj.mask(value)

    def validate_cep(self, value):
        return validar_cep(value)

    def validate_numero(self, value):
        return validar_numero(value)

class VinculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vinculo
        fields = '__all__'

class PedidoCredencialSerializer(serializers.ModelSerializer):
    nome_pessoafisica = serializers.CharField(source='vinculo.pessoafisica.nome', read_only=True)

    class Meta:
        model = PedidoCredencial
        fields = '__all__'

class ObservacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observacao
        fields = ['id', 'titulo', 'conteudo', 'user_id', 'pedido_credencial']
        read_only_fields = ['id', 'user_id']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)



class EvolucaoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvolucaoPedido
        fields = ['id', 'status_evolucao', 'pedido_credencial', 'user_id']
        read_only_fields = ['id', 'user_id']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.id
        return super().create(validated_data)

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = '__all__'
