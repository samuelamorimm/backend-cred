from django.contrib import admin
from .models import *

# Register your models here.

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
    list_display = ('id', 'nome', 'cpf', 'municipio', 'estado')
    search_fields = ('nome', 'cpf')
    list_filter = ('estado', 'municipio')

@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(admin.ModelAdmin):
    list_display = ('id', 'razao_social', 'cnpj', 'municipio', 'estado')
    search_fields = ('razao_social', 'cnpj')
    list_filter = ('estado', 'municipio')

@admin.register(Vinculo)
class VinculoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cargo', 'pessoafisica', 'pessoajuridica')

@admin.register(PedidoCredencial)
class PedidoCredencialAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_pedido', 'status_pedido', 'vinculo')

@admin.register(EvolucaoPedido)
class EvolucaoPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido_credencial', 'status_evolucao', 'user_id')

@admin.register(Observacao)
class ObservacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'pedido_credencial', 'user_id')

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_documento', 'tipo_documento', 'arquivo', 'pedido_credencial')