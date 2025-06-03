# Documentação de como utilizar a API de Autenticação JWT 

## Base URL
http://localhost:8000/api/

## Endppoints de Autenticação 

### Registro de Usuários

- **Endpoint:** `/register/`
- **Método:** `POST`

Corpo da Requisição (JSON)

- **json:**
{
  "username": "seu_username",
  "email": "seu_email@email.com",
  "password": "sua_senha",
  "password2": "sua_senha"
}

### Login de Usuários

- **Endpoint:** `/login/`
- **Método:** `POST`

Corpo da Requisição (JSON)

- **json:**
{
  "email": "seu_email",
  "password": "sua_senha"
}