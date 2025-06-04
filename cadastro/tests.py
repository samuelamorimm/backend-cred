from django.test import TestCase
from django.core.exceptions import ValidationError
from cadastro.models import PessoaFisica, Estado, Municipio

class PessoaFisicaModelTest(TestCase):

    def setUp(self):
        # Criar estado e município para relacionamento obrigatório
        self.estado = Estado.objects.create(nome="São Paulo", sigla="SP")
        self.municipio = Municipio.objects.create(nome="Campinas", cod_ibge="3509502", estado=self.estado)

    def test_criar_pessoa_fisica_valida(self):
        pessoa = PessoaFisica.objects.create(
            nome="João da Silva",
            data_nascimento="1990-01-01",
            sexo=1,
            estado_civil=2,
            cpf="123.456.789-10",
            rg="123456789",
            org_emissor_rg="SSP",
            data_emissao="2010-01-01",
            nome_mae="Maria da Silva",
            nome_pai="José da Silva",
            naturalidade="Campinas",
            nacionalidade="Brasileiro",
            fone_residencial="(19) 1234-5678",
            fone_celular="(19) 98765-4321",
            email="joao@example.com",
            logradouro="Rua das Flores",
            numero="123",
            complemento="Apto 10",
            bairro="Centro",
            cep="13000-000",
            municipio=self.municipio,
            estado=self.estado,
        )
        self.assertEqual(str(pessoa), "João da Silva")
        self.assertEqual(pessoa.cpf, "123.456.789-10")

    def test_cpf_unico(self):
        PessoaFisica.objects.create(
            nome="João da Silva",
            data_nascimento="1990-01-01",
            sexo=1,
            estado_civil=2,
            cpf="123.456.789-10",
            fone_celular="(19) 98765-4321",
            email="joao@example.com",
            logradouro="Rua das Flores",
            numero="123",
            bairro="Centro",
            cep="13000-000",
            municipio=self.municipio,
            estado=self.estado,
        )
        with self.assertRaises(Exception):  # Pode ser IntegrityError, dependendo do banco
            PessoaFisica.objects.create(
                nome="Maria Souza",
                data_nascimento="1992-02-02",
                sexo=2,
                estado_civil=1,
                cpf="123.456.789-10",  # mesmo CPF duplicado
                fone_celular="(19) 99999-9999",
                email="maria@example.com",
                logradouro="Rua das Palmeiras",
                numero="456",
                bairro="Jardim",
                cep="13001-000",
                municipio=self.municipio,
                estado=self.estado,
            )

    def test_email_valido(self):
        pessoa = PessoaFisica(
            nome="João da Silva",
            data_nascimento="1990-01-01",
            sexo=1,
            estado_civil=2,
            cpf="999.999.999-99",
            fone_celular="(19) 98765-4321",
            email="email_invalido",
            logradouro="Rua das Flores",
            numero="123",
            bairro="Centro",
            cep="13000-000",
            municipio=self.municipio,
            estado=self.estado,
        )
        with self.assertRaises(ValidationError):
            pessoa.full_clean()  # Vai validar o campo email e outros

