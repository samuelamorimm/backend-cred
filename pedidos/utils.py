from app.models import PessoaFisica, Vinculo, PedidoCredencial
from django.utils import timezone

# Criar uma pessoa
pessoa = PessoaFisica.objects.create(
    nome='João da Silva',
    cpf='12345678900',
    data_nascimento='1990-05-15',
    # outros campos se tiver
)

# Criar vínculo
vinculo = Vinculo.objects.create(
    pessoafisica=pessoa,
    empresa='Empresa Exemplo',
    cargo='Analista de Sistemas',
    # outros campos
)

# Criar pedido
pedido = PedidoCredencial.objects.create(
    vinculo=vinculo,
    status='em_análise',
    data_pedido=timezone.now(),
    # outros campos se houver
)

print(f"Pedido criado com id {pedido.id}")