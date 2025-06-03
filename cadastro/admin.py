from django.contrib import admin
from app.models import (
    Estado, Municipio, PessoaFisica, PessoaJuridica, Vinculo,
    PedidoCredencial, EvolucaoPedido, Observacao, Documento
)


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sigla')
    search_fields = ('nome', 'sigla')


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cod_ibge', 'estado')
    search_fields = ('nome', 'cod_ibge')
    list_filter = ('estado',)


@admin.register(PessoaFisica)
class PessoaFisicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'data_nascimento', 'municipio')
    search_fields = ('nome', 'cpf', 'email')
    list_filter = ('municipio', 'estado')


@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'razao_social', 'cnpj', 'municipio')
    search_fields = ('razao_social', 'cnpj')
    list_filter = ('municipio', 'estado')


@admin.register(Vinculo)
class VinculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pessoafisica', 'pessoajuridica', 'cargo', 'data_admissao')
    search_fields = ('cargo',)


@admin.register(PedidoCredencial)
class PedidoCredencialAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_pedido', 'status_pedido', 'vinculo')
    list_filter = ('status_pedido',)


@admin.register(EvolucaoPedido)
class EvolucaoPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido_credencial', 'status_evolucao', 'user')


@admin.register(Observacao)
class ObservacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'pedido_credencial', 'user')


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_documento', 'pedido_credencial', 'tipo_documento')
