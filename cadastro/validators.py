import re
from datetime import date
from rest_framework.exceptions import ValidationError


def validar_cep(cep):
    if not re.match(r'^\d{8}$', cep):
        raise ValidationError("CEP deve conter exatamente 8 dígitos numéricos.")


def validar_telefone(telefone):
    if telefone is None or telefone == '':
        return 
    if not re.match(r'^\d{10,11}$', telefone):
        raise ValidationError("Telefone inválido. Deve conter 10 ou 11 dígitos numéricos.")


def validar_email_personalizado(email):
    # Aqui pode colocar validações extras de domínio, etc.
    # Exemplo para validar domínio específico:
    # if not email.endswith('@email.com'):
    #     raise ValidationError("Email deve ser do domínio '@email.com'.")
    pass  # email básico já é validado pelo EmailField do Django


def validar_datas_nascimento_emissao(data_nascimento, data_emissao):
    if data_emissao and data_emissao < data_nascimento:
        raise ValidationError({"data_emissao": "Data de emissão não pode ser anterior à data de nascimento."})

    hoje = date.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    if idade < 0:
        raise ValidationError({"data_nascimento": "Data de nascimento não pode ser no futuro."})

    # Se quiser obrigar maioridade mínima:
    # if idade < 18:
    #     raise ValidationError({"data_nascimento": "Deve ser maior de 18 anos."})


def validar_cpf(cpf):
    cpf_numeros = re.sub(r'\D', '', cpf)
    if len(cpf_numeros) != 11:
        raise ValidationError("CPF deve conter 11 dígitos numéricos.")




def validar_cnpj(cnpj):
    cnpj_numeros = re.sub(r'\D', '', cnpj)
    if len(cnpj_numeros) != 14:
        raise ValidationError("CNPJ deve conter 14 dígitos numéricos.")




def validar_status_pedido(status):
    status_validos = ['Pendente', 'Aprovado', 'Rejeitado', 'Em Análise']
    if status and status not in status_validos:
        raise ValidationError(f"Status '{status}' inválido. Valores válidos: {', '.join(status_validos)}.")


def validar_renda(renda):
    if renda is not None and renda < 0:
        raise ValidationError("Renda deve ser maior ou igual a zero.")
