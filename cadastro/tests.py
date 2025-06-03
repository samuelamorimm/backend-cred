# cadastro/tests.py

from django.test import TestCase
from app.models import Estado, Municipio, PessoaFisica, PessoaJuridica, Vinculo, PedidoCredencial, EvolucaoPedido, Observacao, Documento

class EstadoModelTest(TestCase):
    def setUp(self):
        self.estado = Estado.objects.create(nome="São Paulo", sigla="SP")

    def test_estado_str(self):
        self.assertEqual(str(self.estado), "São Paulo")

# (Crie os testes para os demais modelos do mesmo jeito, importando do app.models)
# Exemplo de PessoaFisica:

class PessoaFisicaModelTest(TestCase):
    def setUp(self):
        self.estado = Estado.objects.create(nome="São Paulo", sigla="SP")
        self.municipio = Municipio.objects.create(nome="São Paulo", cod_ibge="3550308", estado=self.estado)

    def test_criar_pessoa_fisica(self):
        pessoa = PessoaFisica.objects.create(
            nome="Teste",
            data_nascimento="1990-01-01",
            sexo=1,
            estado_civil=1,
            cpf="12345678909",
            naturalidade="São Paulo",
            nacionalidade="Brasileiro",
            logradouro="Rua Teste",
            numero="123",
            complemento="",
            bairro="Centro",
            cep="12345678",
            fone_celular="11999999999",
            email="teste@email.com",
            municipio=self.municipio,
            estado=self.estado
        )
        self.assertEqual(pessoa.nome, "Teste")
