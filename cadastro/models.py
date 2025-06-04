from django.db import models
from django.contrib.auth import get_user_model

# -------------------------------
# Models de Apoio (Endereço)
# -------------------------------

class Estado(models.Model):
    nome = models.CharField('Nome', max_length=255)
    sigla = models.CharField('Sigla', max_length=2, unique=True)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.nome


class Municipio(models.Model):
    nome = models.CharField('Nome', max_length=255)
    cod_ibge = models.CharField('Código IBGE', max_length=20, unique=True)
    estado = models.ForeignKey(Estado, verbose_name='Estado', on_delete=models.PROTECT, related_name='municipios')

    class Meta:
        verbose_name = 'Município'
        verbose_name_plural = 'Municípios'

    def __str__(self):
        return self.nome


class EnderecoBase(models.Model):
    logradouro = models.CharField('Logradouro', max_length=255)
    numero = models.CharField('Número', max_length=10)
    complemento = models.CharField('Complemento', max_length=255, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=255)
    cep = models.CharField('CEP', max_length=10)
    municipio = models.ForeignKey(Municipio, verbose_name='Município', on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, verbose_name='Estado', on_delete=models.PROTECT)

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
    nome = models.CharField('Nome Completo', max_length=255)
    data_nascimento = models.DateField('Data de Nascimento')
    sexo = models.PositiveSmallIntegerField('Sexo', choices=SEXO_CHOICES)
    estado_civil = models.PositiveSmallIntegerField('Estado Civil', choices=ESTADO_CIVIL_CHOICES)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    rg = models.CharField('RG', max_length=20, null=True, blank=True)
    org_emissor_rg = models.CharField('Orgão Emissor RG', max_length=20, null=True, blank=True)
    data_emissao = models.DateField('Data de Emissão do RG', null=True, blank=True)
    nome_mae = models.CharField('Nome da Mãe', max_length=255, null=True, blank=True)
    nome_pai = models.CharField('Nome do Pai', max_length=255, null=True, blank=True)
    naturalidade = models.CharField('Naturalidade', max_length=255)
    nacionalidade = models.CharField('Nacionalidade', max_length=255)
    fone_residencial = models.CharField('Telefone Residencial', max_length=20, null=True, blank=True)
    fone_celular = models.CharField('Telefone Celular', max_length=20)
    email = models.EmailField('E-mail', max_length=255)

    class Meta:
        verbose_name = 'Pessoa Física'
        verbose_name_plural = 'Pessoas Físicas'

    def __str__(self):
        return self.nome


class PessoaJuridica(EnderecoBase):
    nome_fantasia = models.CharField('Nome Fantasia', max_length=255)
    razao_social = models.CharField('Razão Social', max_length=255)
    cnpj = models.CharField('CNPJ', max_length=18, unique=True)
    insc_estadual = models.CharField('Inscrição Estadual', max_length=45, null=True, blank=True)
    cod_cnae = models.CharField('CNAE', max_length=20, null=True, blank=True)
    fone = models.CharField('Telefone', max_length=20, null=True, blank=True)
    nome_responsavel = models.CharField('Nome do Responsável', max_length=255)
    email = models.EmailField('E-mail', max_length=255)

    class Meta:
        verbose_name = 'Pessoa Jurídica'
        verbose_name_plural = 'Pessoas Jurídicas'

    def __str__(self):
        return self.razao_social


# -------------------------------
# Models de Vínculo e Credencial
# -------------------------------

class Vinculo(models.Model):
    cargo = models.CharField('Cargo', max_length=255)
    data_admissao = models.DateField('Data de Admissão')
    renda = models.DecimalField('Renda', max_digits=15, decimal_places=2)
    num_ctps = models.CharField('Número da CTPS', max_length=20)
    pis_pasep = models.CharField('PIS/PASEP', max_length=20, null=True, blank=True)
    fone_comercial = models.CharField('Telefone Comercial', max_length=20)
    pessoajuridica = models.ForeignKey(PessoaJuridica, verbose_name='Pessoa Jurídica', on_delete=models.PROTECT, related_name='vinculos')
    pessoafisica = models.ForeignKey(PessoaFisica, verbose_name='Pessoa Física', on_delete=models.PROTECT, related_name='vinculos')

    class Meta:
        verbose_name = 'Vínculo'
        verbose_name_plural = 'Vínculos'

    def __str__(self):
        return f"{self.pessoafisica.nome} - {self.cargo}"


STATUS_PEDIDO_CHOICES = (
    ('PENDENTE', 'Pendente'),
    ('APROVADO', 'Aprovado'),
    ('REPROVADO', 'Reprovado'),
    ('CANCELADO', 'Cancelado'),
)


class PedidoCredencial(models.Model):
    data_pedido = models.DateTimeField('Data do Pedido', auto_now_add=True)
    status_pedido = models.CharField('Status do Pedido', max_length=20, choices=STATUS_PEDIDO_CHOICES, default='PENDENTE')
    vinculo = models.ForeignKey(Vinculo, verbose_name='Vínculo', on_delete=models.PROTECT, related_name='pedidos_credencial')

    class Meta:
        verbose_name = 'Pedido de Credencial'
        verbose_name_plural = 'Pedidos de Credencial'

    def __str__(self):
        return f"Pedido #{self.id}"


STATUS_EVOLUCAO_CHOICES = (
    ('RECEBIDO', 'Recebido'),
    ('EM_ANALISE', 'Em Análise'),
    ('APROVADO', 'Aprovado'),
    ('REPROVADO', 'Reprovado'),
)


class EvolucaoPedido(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name='Usuário', on_delete=models.SET_NULL, null=True, blank=True)
    status_evolucao = models.CharField('Status da Evolução', max_length=20, choices=STATUS_EVOLUCAO_CHOICES, default='RECEBIDO')
    pedido_credencial = models.ForeignKey(PedidoCredencial, verbose_name='Pedido de Credencial', on_delete=models.PROTECT, related_name='evolucoes')

    class Meta:
        verbose_name = 'Evolução do Pedido'
        verbose_name_plural = 'Evoluções do Pedido'

    def __str__(self):
        return f"Evolução #{self.id} do Pedido #{self.pedido_credencial.id}"


class Observacao(models.Model):
    titulo = models.CharField('Título', max_length=255, null=True, blank=True)
    conteudo = models.TextField('Conteúdo', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), verbose_name='Usuário', on_delete=models.SET_NULL, null=True, blank=True)
    pedido_credencial = models.ForeignKey(PedidoCredencial, verbose_name='Pedido de Credencial', on_delete=models.PROTECT, related_name='observacoes')

    class Meta:
        verbose_name = 'Observação'
        verbose_name_plural = 'Observações'

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
    nome_documento = models.CharField('Nome do Documento', max_length=255)
    nome_arquivo = models.CharField('Nome do Arquivo', max_length=255)
    extensao_arquivo = models.CharField('Extensão do Arquivo', max_length=10)
    tamanho_arquivo = models.CharField('Tamanho do Arquivo', max_length=20)
    tipo_documento = models.CharField('Tipo de Documento', max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    conteudo = models.BinaryField('Conteúdo')
    pedido_credencial = models.ForeignKey(PedidoCredencial, verbose_name='Pedido de Credencial', on_delete=models.PROTECT, related_name='documentos')

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return self.nome_documento
