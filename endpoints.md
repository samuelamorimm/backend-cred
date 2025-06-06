# Documentação dos Endpoints

## Pedidos de Credencial

### Listar Pedidos
- **Endpoint**: `GET /pedidos-credencial/`
- **Descrição**: Retorna a lista de todos os pedidos de credencial
- **Resposta**: Lista de pedidos com seus respectivos dados

### Detalhes do Pedido
- **Endpoint**: `GET /pedidos-credencial/{id}/`
- **Descrição**: Retorna os detalhes de um pedido específico
- **Parâmetros**: 
  - `id`: ID do pedido
- **Resposta**: Dados completos do pedido

### Criar Pedido
- **Endpoint**: `POST /pedidos-credencial/`
- **Descrição**: Cria um novo pedido de credencial
- **Corpo da Requisição**:
  ```json
  {
    "data_pedido": "2024-03-14T10:00:00Z",
    "status_pedido": "PENDENTE",
    "vinculo": 1
  }
  ```

### Atualizar Pedido
- **Endpoint**: `PUT /pedidos-credencial/{id}/`
- **Descrição**: Atualiza um pedido existente
- **Parâmetros**: 
  - `id`: ID do pedido
- **Corpo da Requisição**: Mesmo formato do criar

### Deletar Pedido
- **Endpoint**: `DELETE /pedidos-credencial/{id}/`
- **Descrição**: Remove um pedido
- **Parâmetros**: 
  - `id`: ID do pedido

## Observações

### Listar Observações
- **Endpoint**: `GET /observacoes/`
- **Descrição**: Retorna a lista de observações
- **Parâmetros de Query**:
  - `pedido_id`: ID do pedido para filtrar observações (opcional)
- **Autenticação**: Requerida

### Criar Observação
- **Endpoint**: `POST /observacoes/`
- **Descrição**: Cria uma nova observação
- **Autenticação**: Requerida
- **Corpo da Requisição**:
  ```json
  {
    "titulo": "Título da Observação",
    "conteudo": "Conteúdo da observação",
    "pedido_credencial": 1
  }
  ```

### Atualizar Observação
- **Endpoint**: `PUT /observacoes/{id}/`
- **Descrição**: Atualiza uma observação existente
- **Autenticação**: Requerida
- **Parâmetros**: 
  - `id`: ID da observação

### Deletar Observação
- **Endpoint**: `DELETE /observacoes/{id}/`
- **Descrição**: Remove uma observação
- **Autenticação**: Requerida
- **Parâmetros**: 
  - `id`: ID da observação

## Evoluções do Pedido

### Listar Evoluções
- **Endpoint**: `GET /evolucoes/`
- **Descrição**: Retorna a lista de evoluções
- **Parâmetros de Query**:
  - `pedido_id`: ID do pedido para filtrar evoluções (opcional)
- **Autenticação**: Requerida

### Última Evolução
- **Endpoint**: `GET /evolucoes/ultima_evolucao/`
- **Descrição**: Retorna a última evolução de um pedido
- **Parâmetros de Query**:
  - `pedido_id`: ID do pedido (obrigatório)
- **Autenticação**: Requerida

### Criar Evolução
- **Endpoint**: `POST /evolucoes/`
- **Descrição**: Cria uma nova evolução
- **Autenticação**: Requerida
- **Corpo da Requisição**:
  ```json
  {
    "status_evolucao": "EM_ANALISE",
    "pedido_credencial": 1
  }
  ```

### Atualizar Evolução
- **Endpoint**: `PUT /evolucoes/{id}/`
- **Descrição**: Atualiza uma evolução existente
- **Autenticação**: Requerida
- **Parâmetros**: 
  - `id`: ID da evolução

### Deletar Evolução
- **Endpoint**: `DELETE /evolucoes/{id}/`
- **Descrição**: Remove uma evolução
- **Autenticação**: Requerida
- **Parâmetros**: 
  - `id`: ID da evolução

## Relatórios

### Exportar CSV
- **Endpoint**: `GET /exportar/pedidos.csv`
- **Descrição**: Gera um arquivo CSV com todos os pedidos
- **Resposta**: Arquivo CSV com os seguintes campos:
  - ID
  - Data Pedido
  - Status
  - Nome Pessoa
  - Empresa

### Exportar PDF
- **Endpoint**: `GET /exportar/pedidos.pdf`
- **Descrição**: Gera um arquivo PDF com todos os pedidos
- **Resposta**: Arquivo PDF contendo:
  - Título do relatório
  - Lista de pedidos com:
    - ID
    - Data
    - Status
    - Nome da Pessoa
    - Empresa

## Status dos Pedidos

### Atualizar Status
- **Endpoint**: `POST /pedido/{pedido_id}/atualizar-status/`
- **Descrição**: Atualiza o status de um pedido específico
- **Parâmetros**: 
  - `pedido_id`: ID do pedido
- **Corpo da Requisição**:
  ```json
  {
    "status": "APROVADO"
  }
  ```
- **Status Possíveis**:
  - PENDENTE
  - EM_ANALISE
  - APROVADO
  - REJEITADO
  - CANCELADO 