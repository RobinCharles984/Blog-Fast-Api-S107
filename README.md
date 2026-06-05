# Blog FastAPI - CI/CD com Jenkins e Docker

## Sobre o Projeto

Este projeto foi desenvolvido com foco na implementação de uma infraestrutura de Integração Contínua e Entrega Contínua (CI/CD) utilizando Jenkins, Docker e Docker Hub.

A aplicação consiste em uma API REST desenvolvida com FastAPI e executada em um ambiente containerizado composto por múltiplos serviços.

O principal objetivo do projeto foi automatizar o ciclo de build, testes, empacotamento, publicação e notificação através de uma pipeline Jenkins totalmente versionada em código.

---

# Tecnologias Utilizadas

* Python
* FastAPI
* Pytest
* PostgreSQL
* MinIO
* Nginx
* PgAdmin
* Docker
* Docker Compose
* Jenkins
* Docker Hub

---

# Arquitetura

```text
GitHub
   │
   ▼
Jenkins Pipeline
   │
   ├── Checkout
   ├── Install Dependencies
   ├── Compile Application
   ├── Build Docker Image
   ├── Package Application
   ├── Run Tests
   ├── Docker Push
   ├── Archive Artifacts
   └── Email Notification
   │
   ▼
Docker Hub
```

---

# Containers Utilizados

O ambiente completo é composto pelos seguintes containers:

| Container   | Função                      |
| ----------- | --------------------------- |
| FastAPI App | Aplicação principal         |
| PostgreSQL  | Banco de dados              |
| MinIO       | Armazenamento de objetos    |
| Nginx       | Proxy reverso               |
| PgAdmin     | Administração do PostgreSQL |
| Jenkins     | Pipeline CI/CD              |

O projeto atende aos requisitos de:

* Mais de 4 containers;
* Comunicação entre containers;
* Uso de Dockerfile próprio;
* Uso de imagens oficiais do Docker Hub;
* Persistência via volumes Docker.

---

# Pipeline CI/CD

A pipeline foi implementada exclusivamente através de um Jenkinsfile armazenado no repositório.

## Etapas Executadas

### Checkout

Obtém automaticamente o código-fonte do GitHub.

### Install Dependencies

Cria um ambiente virtual Python e instala as dependências necessárias.

### Compile Application

Realiza validação sintática da aplicação.

```bash
python -m py_compile main.py
```

### Build Docker Image

Constrói a imagem Docker da aplicação.

```bash
docker build
```

### Package Application

Gera um pacote compactado da aplicação.

```bash
tar -czf blog-fastapi-${BUILD_NUMBER}.tar.gz
```

### Run Tests

Executa os testes automatizados.

```bash
pytest --junitxml=test-results.xml
```

### Docker Push

Publica automaticamente a imagem da aplicação no Docker Hub.

### Archive Artifacts

Armazena os artefatos da build.

### Email Notification

Envia notificação automática de sucesso ou falha.

---

# Artefatos Gerados

A pipeline armazena automaticamente:

## Relatório de Testes

```text
test-results.xml
```

## Pacote da Aplicação

```text
blog-fastapi-<build>.tar.gz
```

Ambos ficam disponíveis para download diretamente na interface do Jenkins.

---

# Docker Hub

## Jenkins Customizado

Imagem Docker contendo:

* Jenkins pré-configurado
* Docker CLI instalada
* Plugins necessários para CI/CD
* Jenkins Configuration as Code (JCasC)

Docker Hub:

```text
https://hub.docker.com/r/pizzonin/blog-jenkins
```

---

## Aplicação FastAPI

Imagem gerada automaticamente pela pipeline.

Docker Hub:

```text
https://hub.docker.com/r/pizzonin/blog-fastapi-app
```

---

# Executando o Jenkins Diretamente do Docker Hub

A imagem do Jenkins pode ser executada independentemente do restante da infraestrutura.

## Baixar a imagem

```bash
docker pull pizzonin/blog-jenkins:latest
```

## Executar o container

```bash
docker run -d --name jenkins-test --user root -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock --env-file .env pizzonin/blog-jenkins:latest
```

## Acessar Jenkins

```text
http://localhost:8080
```

---

## Obter a senha inicial

```bash
docker exec jenkins-test cat /var/jenkins_home/secrets/initialAdminPassword
```

---

# Executando Toda a Infraestrutura

Subir todos os serviços:

```bash
docker compose up -d
```

Verificar containers:

```bash
docker ps
```

Parar os containers:

```bash
docker compose down
```

Remover containers e volumes:

```bash
docker compose down -v
```

---

# Estrutura de CI/CD

O Jenkins utiliza:

* Jenkinsfile versionado;
* Docker Socket para execução de builds Docker;
* Docker Hub para distribuição das imagens;
* Credentials gerenciadas via Jenkins Configuration as Code;
* Notificações por e-mail parametrizadas por variáveis de ambiente.

Nenhuma etapa da pipeline foi criada manualmente pela interface gráfica do Jenkins.

---

# Jenkins Configuration as Code (JCasC)

O Jenkins é configurado automaticamente através do arquivo:

```text
jenkins/casc/jenkins.yaml
```

A configuração inclui:

* Credenciais Docker Hub;
* Configuração SMTP;
* Configuração de e-mail;
* URL da instância Jenkins.

Os segredos não ficam armazenados na imagem Docker, sendo fornecidos através de variáveis de ambiente.

---

# Requisitos Atendidos

* Pipeline implementada via Jenkinsfile;
* Execução automatizada de testes;
* Build automatizada;
* Empacotamento da aplicação;
* Armazenamento de artefatos;
* Relatório de testes armazenado;
* Publicação no Docker Hub;
* Notificação automática por e-mail;
* Jenkins configurado via código;
* Infraestrutura containerizada;
* Comunicação entre containers;
* Persistência via volumes;
* Imagem Docker customizada do Jenkins;
* Imagem Docker da aplicação publicada automaticamente.

---
