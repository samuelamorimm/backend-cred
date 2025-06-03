from rest_framework import viewsets
from app.models import (
    Estado, Municipio, PessoaFisica, PessoaJuridica, Vinculo,
    PedidoCredencial, EvolucaoPedido, Observacao, Documento
)
from .serializers import (
    EstadoSerializer, MunicipioSerializer, PessoaFisicaSerializer,
    PessoaJuridicaSerializer, VinculoSerializer, PedidoCredencialSerializer,
    EvolucaoPedidoSerializer, ObservacaoSerializer, DocumentoSerializer
)


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
