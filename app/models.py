from django.db import models
from django.contrib.auth import get_user_model

# -------------------------------
# Models de Apoio (Endereço)
# -------------------------------

class Estado(models.Model):
    nome = models.CharField(max_length=255)
    sigla = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.nome


class Municipio(models.Model):
    nome = models.CharField(max_length=255)
    cod_ibge = models.CharField(max_length=20, unique=True)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='municipios')

    def __str__(self):
        return self.nome


class EnderecoBase(models.Model):
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255)
    cep = models.CharField(max_length=10)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    class Meta:
        abstract = True


# -------------------------------
# Models de Pessoas
# -------------------------------

SEXO_CHOICES = (
    (1, 'Masculino'),
    (2, 'Feminino'),
    (3, 'Outro'),
)

ESTADO_CIVIL_CHOICES = (
    (1, 'Solteiro(a)'),
    (2, 'Casado(a)'),
    (3, 'Divorciado(a)'),
    (4, 'Viúvo(a)'),
    (5, 'Separado(a)'),
)


class PessoaFisica(EnderecoBase):
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    sexo = models.PositiveSmallIntegerField(choices=SEXO_CHOICES)
    estado_civil = models.PositiveSmallIntegerField(choices=ESTADO_CIVIL_CHOICES)
    cpf = models.CharField(max_length=14, unique=True)  # 000.000.000-00
    rg = models.CharField(max_length=20, null=True, blank=True)
    org_emissor_rg = models.CharField(max_length=20, null=True, blank=True)
    data_emissao = models.DateField(null=True, blank=True)
    nome_mae = models.CharField(max_length=255, null=True, blank=True)
    nome_pai = models.CharField(max_length=255, null=True, blank=True)
    naturalidade = models.CharField(max_length=255)
    nacionalidade = models.CharField(max_length=255)
    fone_residencial = models.CharField(max_length=20, null=True, blank=True)
    fone_celular = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.nome


class PessoaJuridica(EnderecoBase):
    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True)  # 00.000.000/0000-00
    insc_estadual = models.CharField(max_length=45, null=True, blank=True)
    cod_cnae = models.CharField(max_length=20, null=True, blank=True)
    fone = models.CharField(max_length=20, null=True, blank=True)
    nome_responsavel = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.razao_social


# -------------------------------
# Models de Vínculo e Credencial
# -------------------------------

class Vinculo(models.Model):
    cargo = models.CharField(max_length=255)
    data_admissao = models.DateField()
    renda = models.DecimalField(max_digits=15, decimal_places=2)
    num_ctps = models.CharField(max_length=20)
    pis_pasep = models.CharField(max_length=20, null=True, blank=True)
    fone_comercial = models.CharField(max_length=20)
    pessoajuridica = models.ForeignKey(PessoaJuridica, on_delete=models.PROTECT, related_name='vinculos')
    pessoafisica = models.ForeignKey(PessoaFisica, on_delete=models.PROTECT, related_name='vinculos')

    def __str__(self):
        return f"{self.pessoafisica.nome} - {self.cargo}"


STATUS_PEDIDO_CHOICES = (
    ('PENDENTE', 'Pendente'),
    ('APROVADO', 'Aprovado'),
    ('REPROVADO', 'Reprovado'),
    ('CANCELADO', 'Cancelado'),
)


class PedidoCredencial(models.Model):
    data_pedido = models.DateTimeField(auto_now_add=True)
    status_pedido = models.CharField(max_length=20, choices=STATUS_PEDIDO_CHOICES, default='PENDENTE')
    vinculo = models.ForeignKey(Vinculo, on_delete=models.PROTECT, related_name='pedidos_credencial')

    def __str__(self):
        return f"Pedido #{self.id}"


STATUS_EVOLUCAO_CHOICES = (
    ('RECEBIDO', 'Recebido'),
    ('EM_ANALISE', 'Em Análise'),
    ('APROVADO', 'Aprovado'),
    ('REPROVADO', 'Reprovado'),
)


class EvolucaoPedido(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    status_evolucao = models.CharField(max_length=20, choices=STATUS_EVOLUCAO_CHOICES, default='RECEBIDO')
    pedido_credencial = models.ForeignKey(PedidoCredencial, on_delete=models.PROTECT, related_name='evolucoes')

    def __str__(self):
        return f"Evolução #{self.id} do Pedido #{self.pedido_credencial.id}"


class Observacao(models.Model):
    titulo = models.CharField(max_length=255, null=True, blank=True)
    conteudo = models.TextField(null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    pedido_credencial = models.ForeignKey(PedidoCredencial, on_delete=models.PROTECT, related_name='observacoes')

    def __str__(self):
        return self.titulo or f"Obs #{self.id}"


# -------------------------------
# Model de Documentos
# -------------------------------

TIPO_DOCUMENTO_CHOICES = (
    ('PDF', 'PDF'),
    ('IMAGEM', 'Imagem'),
    ('OUTRO', 'Outro'),
)


class Documento(models.Model):
    nome_documento = models.CharField(max_length=255)
    nome_arquivo = models.CharField(max_length=255)
    extensao_arquivo = models.CharField(max_length=10)
    tamanho_arquivo = models.CharField(max_length=20)
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    conteudo = models.BinaryField()  # ✔️ Se quiser, pode trocar para FileField futuramente.
    pedido_credencial = models.ForeignKey(PedidoCredencial, on_delete=models.PROTECT, related_name='documentos')

    def __str__(self):
        return self.nome_documento
