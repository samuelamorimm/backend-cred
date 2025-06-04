from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from .models import PedidoCredencial

# Create your views here.

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

class PessoaFisicaViewSet(viewsets.ModelViewSet):
    queryset = PessoaFisica.objects.all()
    serializer_class = PessoaFisicaSerializer

class PessoaJuridicaViewSet(viewsets.ModelViewSet):
    queryset = PessoaJuridica.objects.all()
    serializer_class = PessoaJuridicaSerializer

class VinculoViewSet(viewsets.ModelViewSet):
    queryset = Vinculo.objects.all()
    serializer_class = VinculoSerializer

class PedidoCredencialViewSet(viewsets.ModelViewSet):
    queryset = PedidoCredencial.objects.all()
    serializer_class = PedidoCredencialSerializer

class EvolucaoPedidoViewSet(viewsets.ModelViewSet):
    queryset = EvolucaoPedido.objects.all()
    serializer_class = EvolucaoPedidoSerializer

class ObservacaoViewSet(viewsets.ModelViewSet):
    queryset = Observacao.objects.all()
    serializer_class = ObservacaoSerializer

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

def export_pedidos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Data Pedido', 'Status', 'Nome Pessoa', 'Empresa'])

    pedidos = PedidoCredencial.objects.select_related('vinculo__pessoafisica', 'vinculo__pessoajuridica').all()

    for pedido in pedidos:
        writer.writerow([
            pedido.id,
            pedido.data_pedido.strftime('%d/%m/%Y %H:%M'),
            pedido.status_pedido,
            pedido.vinculo.pessoafisica.nome if pedido.vinculo.pessoafisica else '',
            pedido.vinculo.pessoajuridica.razao_social if pedido.vinculo.pessoajuridica else ''
        ])

    return response

def export_pedidos_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedidos.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "Relatório de Pedidos")
    y -= 40

    p.setFont("Helvetica", 10)
    pedidos = PedidoCredencial.objects.select_related('vinculo__pessoafisica', 'vinculo__pessoajuridica').all()

    for pedido in pedidos:
        texto = (
            f"ID: {pedido.id} | Data: {pedido.data_pedido.strftime('%d/%m/%Y %H:%M')} "
            f"| Status: {pedido.status_pedido} | "
            f"Pessoa: {pedido.vinculo.pessoafisica.nome if pedido.vinculo.pessoafisica else ''} | "
            f"Empresa: {pedido.vinculo.pessoajuridica.razao_social if pedido.vinculo.pessoajuridica else ''}"
        )
        p.drawString(50, y, texto)
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    return response