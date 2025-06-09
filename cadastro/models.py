from django.db import models

class Estado(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    sigla = models.CharField(max_length=2)

    def __str__(self):
        return self.nome


class Municipio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    cod_ibge = models.CharField(max_length=45, unique=True, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING, related_name='municipios')

    def __str__(self):
        return self.nome or 'Município sem nome'


class PessoaFisica(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    sexo = models.PositiveSmallIntegerField()
    estado_civil = models.PositiveSmallIntegerField()
    cpf = models.CharField(max_length=45, unique=True)
    rg = models.CharField(max_length=45, null=True, blank=True)
    org_emissor_rg = models.CharField(max_length=45, null=True, blank=True)
    data_emissao = models.DateField(null=True, blank=True)
    nome_mae = models.CharField(max_length=255, null=True, blank=True)
    nome_pai = models.CharField(max_length=255, null=True, blank=True)
    naturalidade = models.CharField(max_length=255)
    nacionalidade = models.CharField(max_length=255)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cep = models.CharField(max_length=45)
    fone_residencial = models.CharField(max_length=45, null=True, blank=True)
    fone_celular = models.CharField(max_length=45)
    email = models.EmailField(max_length=255)
    municipio = models.ForeignKey(Municipio, on_delete=models.DO_NOTHING, related_name='pessoas_fisicas')
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING, related_name='pessoas_fisicas')

    def __str__(self):
        return self.nome


class PessoaJuridica(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=45, unique=True)
    insc_estadual = models.CharField(max_length=45, null=True, blank=True)
    cod_cnae = models.CharField(max_length=255, null=True, blank=True)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    cep = models.CharField(max_length=45)
    fone = models.CharField(max_length=45, null=True, blank=True)
    nome_responsavel = models.CharField(max_length=45)
    email = models.EmailField(max_length=255)
    municipio = models.ForeignKey(Municipio, on_delete=models.DO_NOTHING, related_name='pessoas_juridicas')
    estado = models.ForeignKey(Estado, on_delete=models.DO_NOTHING, related_name='pessoas_juridicas')

    def __str__(self):
        return self.razao_social


class Vinculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    cargo = models.CharField(max_length=255)
    data_admissao = models.DateField()
    renda = models.DecimalField(max_digits=15, decimal_places=2)
    num_ctps = models.CharField(max_length=45)
    pis_pasep = models.CharField(max_length=45, null=True, blank=True)
    fone_comercial = models.CharField(max_length=45)
    pessoajuridica = models.ForeignKey(PessoaJuridica, on_delete=models.DO_NOTHING, related_name='vinculos')
    pessoafisica = models.ForeignKey(PessoaFisica, on_delete=models.DO_NOTHING, related_name='vinculos')

    def __str__(self):
        return f"{self.pessoafisica.nome} - {self.cargo}"


class PedidoCredencial(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANALISE', 'Em Análise'),
        ('APROVADO', 'Aprovado'),
        ('REJEITADO', 'Rejeitado'),
        ('CANCELADO', 'Cancelado'),
    ]

    id = models.BigAutoField(primary_key=True)
    data_pedido = models.DateTimeField()
    status_pedido = models.CharField(max_length=45, choices=STATUS_CHOICES, default='PENDENTE', null=True, blank=True)
    vinculo = models.ForeignKey(Vinculo, on_delete=models.DO_NOTHING, related_name='pedidos_credencial')

    def __str__(self):
        return f"Pedido #{self.id}"


class EvolucaoPedido(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    status_evolucao = models.CharField(max_length=45, null=True, blank=True)
    pedido_credencial = models.ForeignKey(PedidoCredencial, on_delete=models.DO_NOTHING, related_name='evolucoes')

    def __str__(self):
        return f"Evolução #{self.id} do Pedido #{self.pedido_credencial.id}"


class Observacao(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255, null=True, blank=True)
    conteudo = models.TextField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    pedido_credencial = models.ForeignKey(PedidoCredencial, on_delete=models.DO_NOTHING, related_name='observacoes')

    def __str__(self):
        return self.titulo or f"Obs #{self.id}"


def upload_to_documento(instance, filename):
    return f'documentos/{instance.pedido_credencial.id}/{filename}'

class Documento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome_documento = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=45)
    arquivo = models.FileField(upload_to=upload_to_documento)
    pedido_credencial = models.ForeignKey(PedidoCredencial, on_delete=models.DO_NOTHING, related_name='documentos')


    def __str__(self):
        return self.nome_documento