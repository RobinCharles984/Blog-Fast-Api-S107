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


# Uso de Inteligência Artificial

Em conformidade com os requisitos do projeto, declaramos abaixo o uso transparente de ferramentas de Inteligência Artificial durante o ciclo de desenvolvimento da nossa infraestrutura DevOps.

## Modelos Utilizados
* Gemini (Google)
* GPT-5.5
* Claude
* [INSERIR OUTROS MODELOS USADOS PELO GRUPO: ex: ChatGPT/GPT-4, Claude, GitHub Copilot]

## Finalidades do Uso
A IA foi utilizada para acelerar processos de infraestrutura e validação, especificamente nas seguintes áreas:
* **Geração e otimização do Dockerfile** da aplicação FastAPI.
* **Estruturação inicial e sintaxe declarativa do Jenkinsfile** para os primeiros stages e correções em stages posteriores.
* **Tutorial de push do contâiner Jenkins no dockerhub** para possuir uma imagem jenkins com os plugins instalados
* **Debugging de erros** de conexão do Docker Daemon em ambiente Windows/WSL.
* **Boa parte deste README.md**, tendo algumas alterações e gerado dentro do ambiente da LLM usada.
* **Ideias**, através da IA, foi estudado ideias de implementações como containers que ajudariam a aplicação
* [INSERIR OUTRAS FINALIDADES: ex: geração de fixtures para pytest, formatação do docker-compose.yml]

## Dinâmica de Uso
A IA foi utilizada de forma individual pelos integrantes em suas respectivas frentes de atuação (ex: Integrante 1 para Backend/Build, Integrante 3 para Compose), atuando como um "pair programmer" assíncrono para revisar configurações de infraestrutura antes dos commits. Toda sugestão de código foi revisada e testada localmente antes de ser integrada à pipeline principal, já que alterações sem revisão poderiam levar à quebra do pipe de CI/CD, por exemplo.

## Exemplos Reais de Prompts

Conforme exigido, abaixo estão pelo menos 3 exemplos de prompts utilizados pela equipe e como lidamos com as respostas:

### Exemplo 1: Otimização do Dockerfile (Integrante 1)
* **Prompt:** *"A aplicação já está pronta em FastAPI. O db.py usa BaseSettings e o auth.py usa dependências injetadas. Como posso fazer o Dockerfile ideal para essa aplicação para integrar com o Jenkins depois?"*
* **Resultado:** A IA sugeriu um `Dockerfile` utilizando a imagem `python:3.10-slim` com separação em camadas (copiando o `requirements.txt` primeiro para aproveitar o cache do Docker).
* **Ação:** **Aceito e ajustado.** A estrutura base foi aceita, mas validamos a necessidade de manter a variável de ambiente `ENV PYTHONPATH=.` para garantir o funcionamento correto dos imports dos nossos módulos internos.

### Exemplo 2: Correção do Jenkinsfile
* **Prompt:** *"Eu estou com dois dockerfiles, o da aplicação e um Dockerfile.jenkins que copiei do repositório base que instala nodejs, xvfb e libgtk. Está correto para o meu projeto FastAPI?"*
* **Resultado:** A IA identificou que o modelo copiado era para testes frontend (Cypress) e alertou que nosso projeto precisava de Python nativo no container do Jenkins para rodar o `pip install`.
* **Ação:** **Aceito.** Descartamos o arquivo antigo e reescrevemos o `Dockerfile.jenkins` removendo as bibliotecas gráficas e instalando pacotes de ambiente virtual Python (`python3-venv`).

### Exemplo 3: Configuração e Inicialização do Container Jenkins (Integrante 4)
* **Prompt:** *"Estou tentando subir o Jenkins em um container Docker, mas a pipeline não consegue executar comandos Docker. Como devo iniciar o container?"* 
* **Resultado:** A IA identificou que o Jenkins estava sendo executado sem acesso ao Docker do host. Foi sugerido iniciar o container utilizando o mapeamento do socket Docker (/var/run/docker.sock) e persistir os dados do Jenkins em um volume dedicado.  
* **Ação:** **Aceito.** O comando de inicialização do Jenkins foi atualizado para incluir o volume de persistência e o mapeamento do socket Docker. Após a alteração, o Jenkins passou a conseguir executar comandos Docker dentro das pipelines, permitindo a construção e execução das imagens da aplicação durante o processo de CI/CD. 

## O que NÃO foi feito por IA (Desenvolvimento "À Mão")
Para garantir o domínio técnico exigido, as seguintes partes foram desenvolvidas e configuradas manualmente pela equipe:
* A lógica de negócio e os endpoints principais da aplicação FastAPI.
* A configuração das credenciais e variáveis de ambiente reais no Jenkins (via interface e JCasC).
* A divisão de arquitetura e a decisão de como os volumes seriam mapeados no `docker-compose.yml`.
* A execução e o troubleshooting final da pipeline rodando os 4 containers simultaneamente na máquina local.
* Avaliação da execução correta do pipe de CI/CD.

-- Felipe Zeferino - Seção Uso de IA --

Usado o Codex, baseado em GPT-5, no harness Codex Desktop/App, com acesso ao workspace local do projeto `Blog-Fast-Api-S107`.

A IA auxiliou na configuração de CI/CD com Jenkins, Docker Compose e Jenkins Configuration as Code. O trabalho principal foi implementar notificações por e-mail via Brevo, configurar credenciais do Docker Hub, ajustar o `Jenkinsfile` e validar a pipeline local.

Foram usados terminal local, navegador integrado, Docker, Jenkins em `localhost:8080`, Git e automação de browser. As credenciais SMTP e Docker Hub ficaram no `.env`, sem commit no repositório.

Com apoio da IA, configurei:
- SMTP Brevo via JCasC;
- notificações de sucesso e falha no Jenkins;
- credencial `dockerhub-credentials` via YAML;
- ambiente de teste no pipeline;
- build e push da imagem Docker;
- validação da entrega de e-mail com sender verificado.

Durante o processo, a IA também ajudou a corrigir erros de pipeline, como dependências Python, variáveis de ambiente ausentes, plugin `pytest-cov`, formato de URL S3 nos testes e credencial Docker Hub ausente.

Resultado final: a build do Jenkins passou com sucesso, os testes executaram, a imagem foi publicada no Docker Hub e o e-mail de notificação foi recebido.
