from cadastro.models import Estado, Municipio, PessoaFisica, PessoaJuridica, Vinculo, PedidoCredencial, Documento, EvolucaoPedido, Observacao
from django.utils import timezone

# Estado e Município
estado = Estado.objects.create(nome='Paraná', sigla='PR')
municipio = Municipio.objects.create(nome='Curitiba', cod_ibge='4106902', estado=estado)

# Pessoa Física
pf = PessoaFisica.objects.create(
    nome='Maria Oliveira',
    data_nascimento='1985-10-20',
    sexo=2,
    estado_civil=1,
    cpf='12345678901',
    rg='11223344',
    org_emissor_rg='SSP',
    data_emissao='2002-05-20',
    nome_mae='Joana Oliveira',
    nome_pai='Carlos Oliveira',
    naturalidade='Curitiba',
    nacionalidade='Brasileira',
    logradouro='Rua das Flores',
    numero='123',
    complemento='Ap 101',
    bairro='Centro',
    cep='80000000',
    fone_residencial='4133334444',
    fone_celular='4199998888',
    email='maria@example.com',
    municipio=municipio,
    estado=estado
)

# Pessoa Jurídica
pj = PessoaJuridica.objects.create(
    nome_fantasia='Tech Solutions',
    razao_social='Tech Solutions LTDA',
    cnpj='12345678000199',
    insc_estadual='1234567',
    cod_cnae='6201-5/01',
    logradouro='Av. Inovação',
    numero='456',
    complemento='Sala 5',
    bairro='Tecnologia',
    cep='80001000',
    fone='4133445566',
    nome_responsavel='Pedro Silva',
    email='contato@tech.com.br',
    municipio=municipio,
    estado=estado
)

# Vínculo
vinculo = Vinculo.objects.create(
    cargo='Desenvolvedora Back-end',
    data_admissao='2020-03-15',
    renda=6500.00,
    num_ctps='1234567',
    pis_pasep='12345678900',
    fone_comercial='4133556677',
    pessoajuridica=pj,
    pessoafisica=pf
)

# Pedido Credencial
pedido = PedidoCredencial.objects.create(
    data_pedido=timezone.now(),
    status_pedido='em_análise',
    vinculo=vinculo
)

# Documento

# Evolução do Pedido
EvolucaoPedido.objects.create(
    user_id=1,
    status_evolucao='enviado',
    pedido_credencial=pedido
)

# Observação
Observacao.objects.create(
    titulo='Observação inicial',
    conteudo='Documento legível e completo.',
    user_id=1,
    pedido_credencial=pedido
)

print(f'✅ Pedido #{pedido.id} criado com sucesso para {pf.nome}')
