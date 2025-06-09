from django.test import TestCase
from cadastro.models import Estado, Municipio
from cadastro.serializers import PessoaFisicaSerializer, PessoaJuridicaSerializer
from datetime import date, timedelta

class SerializerGeralTest(TestCase):
    def setUp(self):
        self.estado = Estado.objects.create(nome='São Paulo', sigla='SP')
        self.municipio = Municipio.objects.create(nome='São Paulo', estado=self.estado)
        
        # Dados válidos base para Pessoa Física
        self.pf_data = {
            'nome': 'Fulano de Tal',
            'data_nascimento': '1990-01-01',
            'sexo': 1,
            'estado_civil': 1,
            'cpf': '12345678909',  # Use um CPF válido para seus testes
            'rg': '12345678909',
            'org_emissor_rg': '',
            'data_emissao': None,
            'nome_mae': '',
            'nome_pai': '',
            'naturalidade': 'São Paulo',
            'nacionalidade': 'Brasileiro',
            'logradouro': 'Rua Exemplo',
            'numero': '123',
            'complemento': 'Apto 1',
            'bairro': 'Centro',
            'cep': '01001000',
            'fone_residencial': '11999999999',
            'fone_celular': '11999999999',
            'email': 'fulano@example.com',
            'municipio': self.municipio.id,
            'estado': self.estado.id,
        }
        
        # Dados válidos base para Pessoa Jurídica
        self.pj_data = {
            'nome_fantasia': 'Empresa X',
            'razao_social': 'Empresa X Ltda',
            'cnpj': '12345678000195',  # Use um CNPJ válido para seus testes
            'insc_estadual': '',
            'cod_cnae': '',
            'logradouro': 'Av Exemplo',
            'numero': '456',
            'complemento': 'Sala 10',
            'bairro': 'Bairro Exemplo',
            'cep': '01002000',
            'fone': '1133334444',
            'nome_responsavel': 'João Responsável',
            'email': 'contato@empresax.com.br',
            'municipio': self.municipio.id,
            'estado': self.estado.id,
        }

    def test_pessoa_fisica_valida(self):
        serializer = PessoaFisicaSerializer(data=self.pf_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        validated = serializer.validated_data
        print("\nPessoa Física validada:")
        for key, value in validated.items():
            print(f"  {key}: {value}")
            
        self.assertEqual(validated['cpf'], '123.456.789-09')  # CPF mascarado

    def test_pessoa_fisica_cpf_invalido(self):
        data = self.pf_data.copy()
        data['cpf'] = '12345678900'  # CPF inválido
        serializer = PessoaFisicaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('cpf', serializer.errors)
        self.assertEqual(serializer.errors['cpf'][0], 'CPF inválido')

    def test_pessoa_fisica_data_nascimento_futura(self):
        data = self.pf_data.copy()
        data['data_nascimento'] = (date.today() + timedelta(days=1)).isoformat()
        serializer = PessoaFisicaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('data_nascimento', serializer.errors)
        self.assertEqual(serializer.errors['data_nascimento'][0], 'A data de nascimento não pode ser no futuro.')

    def test_pessoa_juridica_valida(self):
        serializer = PessoaJuridicaSerializer(data=self.pj_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        validated = serializer.validated_data
        print("\nPessoa Jurídica validada:")
        for key, value in validated.items():
            print(f"  {key}: {value}")
        
        self.assertEqual(validated['cnpj'], '12.345.678/0001-95')  # CNPJ mascarado

    def test_pessoa_juridica_cnpj_invalido(self):
        data = self.pj_data.copy()
        data['cnpj'] = '12345678000100'  # CNPJ inválido
        serializer = PessoaJuridicaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('cnpj', serializer.errors)
        self.assertEqual(serializer.errors['cnpj'][0], 'CNPJ inválido')
