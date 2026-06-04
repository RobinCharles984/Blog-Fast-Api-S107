# Blog API - FastAPI

## Descrição

Projeto de uma API REST para gerenciamento de um blog, utilizando as seguintes tecnologias:

* **FastAPI**: Framework principal para construção da API.
* **SQLAlchemy**: ORM para manipulação do banco de dados.
* **Alembic**: Controle de migrações.
* **Pydantic**: Validação e serialização de dados.
* **JWT**: Autenticação baseada em tokens.
* **boto3**: Integração com AWS S3 para armazenamento de imagens.
* **pytest**: Framework de testes.

A documentação interativa da API está disponível automaticamente pelo Swagger em `/docs`.

## Funcionalidades

* Cadastro e login de usuários, com autenticação via JWT.
* CRUD de posts com upload de imagens para AWS S3.
* Controle de permissão para exclusão e atualização de posts.
* Manipulação de arquivos no S3 ao editar ou excluir posts.
* Testes automatizados com pytest.

## Estrutura de Pastas

```
blog/
├── alembic/
├── app/
│   ├── models/
│   │   ├── users.py
│   │   └── posts.py
│   ├── repositories/
│   │   ├── jwt_repo.py
│   │   ├── posts_repo.py
│   │   └── user_repo.py
│   ├── routes/
│   │   ├── posts.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── authentication_schema.py
│   │   ├── base_schema.py
│   │   └── posts_schema.py
│   ├── utils/
│   │   └── s3_utils.py
├── dependencies/
│   ├── auth.py
│   └── db.py
├── exceptions/
│   └── http_exceptions.py
├── tests/
│   ├── conftest.py
│   ├── test_posts.py
│   └── test_users.py
├── .env.example
├── .gitignore
├── alembic.ini
├── config.py
├── main.py
├── pytest.ini
└── requirements.txt
```

## Rotas Principais

<blockquote>
<strong>⚠️ Importante:</strong> Todas as rotas da API estão prefixadas com <code>/api/v1</code>.<br>
Exemplo: <code>POST /api/v1/signup</code>
</blockquote>


### Autenticação

* **POST** `/signup`: Cadastra um novo usuário.
* **POST** `/login`: Realiza login e retorna o token JWT.
* **PATCH** `/{user_id}/promote`: Rota acessível a administração, para promover outro usuário para admin

### Posts

* **POST** `/posts`: Cria um novo post. Permite o upload de imagem para o S3.
* **GET** `/posts`: Lista todos os posts com paginação.
* **GET** `/posts?post_id=1`: Retorna detalhes de um post específico.
* **PUT** `/posts/{post_id}`: Atualiza um post. Se houver nova imagem, a antiga será removida do S3.
* **DELETE** `/posts/{post_id}`: Exclui um post e a imagem correspondente no S3, se existir.

## Modelos

### Users

| Campo         | Tipo        | Restrições                               |
| ------------- | ----------- | ---------------------------------------- |
| id            | Integer     | PK                                       |
| username      | String(20)  | Único, obrigatório                       |
| email         | String(50)  | Único, obrigatório                       |
| password      | String(128) | Obrigatório                              |
| phone\_number | String(20)  | Único, obrigatório                       |
| first\_name   | String(20)  | Obrigatório                              |
| last\_name    | String(20)  | Obrigatório                              |
| gender        | Enum        | Obrigatório (GenderEnum)                 |
| role          | String      | Default: "user"                          |
| create\_date  | DateTime    | Default: now                             |
| update\_date  | DateTime    | Default: now; atualizado automaticamente |


### Posts

| Campo             | Tipo     | Restrições                               |
| ----------------- | -------- | ---------------------------------------- |
| id                | Integer  | PK                                       |
| title             | String   | Obrigatório                              |
| author\_id        | Integer  | FK para Users(id)                        |
| cover\_image\_url | String   | Opcional                                 |
| content           | Text     | Obrigatório                              |
| create\_date      | DateTime | Default: now                             |
| update\_date      | DateTime | Default: now; atualizado automaticamente |


## Dependências importantes

* `.env`: Arquivo para variáveis de ambiente (não enviado ao GitHub).
* `config.py`: Configurações gerais do projeto.
* `requirements.txt`: Dependências do Python.

## Testes

Testes automatizados com **pytest** localizados na pasta `tests/`.

## CI/CD e notificações por email

O Jenkins é configurado via **Configuration as Code** em
`jenkins/casc/jenkins.yaml`. O arquivo usa variáveis de ambiente definidas no
`docker-compose.yml` e documentadas no `.env.example`.

Para habilitar o envio de email, configure no `.env`:

* `EMAIL_RECIPIENTS`: destinatários das notificações.
* `SMTP_HOST` e `SMTP_PORT`: servidor e porta SMTP.
* `SMTP_USERNAME` e `SMTP_PASSWORD`: credenciais SMTP.
* `SMTP_FROM`: remetente usado pelo Jenkins.
* `SMTP_USE_SSL` e `SMTP_USE_TLS`: opções de segurança do provedor SMTP.

O pipeline envia email apenas em caso de sucesso ou falha.

## Execução

1. Clone o repositório
2. Com base no `.env.example`, crie seu `.env`
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute as migrações: `alembic upgrade head`
5. Rode o servidor: `uvicorn main:app --reload`

Acesse a documentação em: `http://localhost:8000/docs`

---

**Autor:** joaopedromsantos

**Licença:** MIT
