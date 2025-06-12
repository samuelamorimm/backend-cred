# 🎫 backend-cred

API backend para gestão de credenciais do SESC – Projeto Integrador.

---

## ✨ Visão Geral

Este projeto é um sistema backend em Django + Django REST Framework para gerenciar pedidos de credencial, usuários, documentos, logs de acesso e status. Ideal para integração com frontend web/mobile!

---

## 🛠️ Tecnologias Utilizadas

- 🐍 **Python 3**
- 🌐 **Django**
- 🔗 **Django REST Framework**
- 🔐 **JWT e Token Auth**
- 📄 **Swagger (drf-yasg)**
- 🗄️ **SQLite** (pronto para trocar por outros bancos)

---

## ⚡ Instalação Rápida

```sh
# 1. Clone o projeto
git clone https://github.com/samuelamorimm/backend-cred.git
cd backend-cred

# 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Migre o banco de dados
python manage.py migrate

# 5. Crie um superusuário
python manage.py createsuperuser

# 6. Rode o servidor
python manage.py runserver
```

---

## 🔑 Autenticação

A API usa autenticação via **Token** ou **JWT**.

### Exemplo de header:
```http
Authorization: Token SEU_TOKEN_AQUI
```

---

## 📚 Documentação Interativa

- [Swagger UI](http://localhost:8000/swagger/)  
- [Redoc](http://localhost:8000/redoc/)

---

## 🚦 Endpoints Principais

### 👤 Usuários

- **Registrar:**  
  `POST /api/register/`  
  ```json
  {
    "username": "usuario",
    "email": "usuario@email.com",
    "password": "senha123",
    "password2": "senha123"
  }
  ```
- **Login:**  
  `POST /api/login/`  
  ```json
  {
    "email": "usuario@email.com",
    "password": "senha123"
  }
  ```

---

### 📋 Pedidos & Cadastro

Todos suportam métodos REST (GET, POST, PUT, DELETE):

- `/api/estados/` — Estados
- `/api/municipios/` — Municípios
- `/api/pessoas-fisicas/` — Pessoas físicas
- `/api/pessoas-juridicas/` — Pessoas jurídicas
- `/api/vinculos/` — Vínculos
- `/api/pedidos-credencial/` — Pedidos de credencial
- `/api/documentos/` — Documentos anexados
- `/api/evolucoes/` — Evolução dos pedidos
- `/api/observacoes/` — Observações em pedidos
- `/api/logs/` — Logs de acesso
- `/api/pessoa-fisica/filtrar/` — Filtro avançado PF
- `/api/pessoa-juridica/filtrar/` — Filtro avançado PJ

#### 📦 Outras rotas úteis
- `POST /api/pedido/<pedido_id>/atualizar-status/` — Atualiza status do pedido
- `GET /api/exportar/pedidos.csv` — Exporta pedidos em CSV
- `GET /api/exportar/pedidos.pdf` — Exporta pedidos em PDF

---

### 🕵️‍♂️ Consulta Pública de Pedido

- **Consultar pedido por CPF e data de nascimento:**  
  `GET /api/consulta/?cpf=00000000000&data=YYYY-MM-DD`
  - *Retorna informações do pedido se existir.*

---

### 🗂️ Upload de Documentos

- **Enviar documento para pedido:**  
  `POST /api/upload/`
  - `pedido_credencial`: ID do pedido (obrigatório)
  - `arquivo`: arquivo (obrigatório)
  - `nome_documento` & `tipo_documento`: opcionais

  Exemplo usando `curl`:
  ```sh
  curl -X POST http://localhost:8000/api/upload/ \
    -H "Authorization: Token SEU_TOKEN_AQUI" \
    -F pedido_credencial=1 \
    -F arquivo=@/caminho/para/arquivo.pdf
  ```

---

## 📝 Exemplo de Fluxo

1. 👤 **Crie um usuário** (`/api/register/`)
2. 🔑 **Faça login** e pegue o token (`/api/login/`)
3. 📝 **Cadastre um pedido de credencial** (`/api/pedidos-credencial/`)
4. 📎 **Anexe documentos** (`/api/upload/`)
5. 👀 **Consulte o status** (`/api/consulta/`)
6. 🔄 **Acompanhe evoluções ou atualize status** (`/api/evolucoes/`, `/api/pedido/<id>/atualizar-status/`)

---

## ⛔ Permissões

- Rotas de login e consulta de pedido são públicas
- Demais rotas exigem autenticação por token

---

## 🧪 Testes

```sh
python manage.py test
```

---

## 🏷️ Licença

MIT License

---

## 💡 Dúvidas?

- Consulte o Swagger para exemplos práticos de cada endpoint!
- Use as issues do repositório para dúvidas ou sugestões!
