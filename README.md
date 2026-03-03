# 🚀 Aura Macless Worker (FindMy)

Worker Python responsável por integração com o ecossistema FindMy
utilizando Anisette Server.

Este projeto roda totalmente via Docker, utilizando **uv** para
gerenciamento moderno de dependências Python.

------------------------------------------------------------------------

## 🏗 Arquitetura

O sistema é composto por 2 containers:

-   **anisette** → Servidor Anisette (autenticação Apple)
-   **aura-worker** → Worker FindMy (este projeto)

Todos rodam na mesma rede Docker:

    mh-network

------------------------------------------------------------------------

## 📦 Pré-requisitos

-   Docker
-   Docker Compose v2+
-   Apple ID válido com 2FA ativado

------------------------------------------------------------------------

## 🐳 Dockerfile

``` dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y     gcc     git     libffi-dev     libssl-dev     && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install uv && uv pip install --system .

EXPOSE 5000

CMD ["python", "main.py"]
```

------------------------------------------------------------------------

## 🌐 Rede Docker

⚠ Dentro do container NÃO use `localhost` para acessar outros serviços.

Use:

    http://anisette:6969

------------------------------------------------------------------------

## 🐳 Executando com Docker Compose

``` bash
docker compose up -d --build
```

Isso irá:

-   Criar a rede automaticamente
-   Subir o Anisette Server
-   Subir o Aura Worker
-   Criar volumes persistentes

------------------------------------------------------------------------

## 🔐 Configuração Apple ID

No docker-compose.yml:

``` yaml
environment:
  - ANISETTE_URL=http://anisette:6969
  - APPLE_ID=seu_email@apple.com
  - APPLE_PWD=sua_senha
```

⚠ Recomenda-se usar arquivo `.env` em produção.

------------------------------------------------------------------------

## 🔌 Portas Expostas

  Serviço       Porta
  ------------- -------
  Anisette      6969
  Aura Worker   5000

API disponível em:

    http://localhost:5000

------------------------------------------------------------------------

## 📁 Volumes Persistentes

-   anisette-v3_data → Dados do Anisette
-   worker_data → Dados do FindMy

------------------------------------------------------------------------

## 🔄 Restart Automático

Todos os serviços usam:

``` yaml
restart: always
```

------------------------------------------------------------------------

## 🧪 Rodando Apenas o Worker

``` bash
docker build -t aura-worker .
docker run -p 5000:5000 aura-worker
```

⚠ Será necessário apontar para um Anisette externo.

------------------------------------------------------------------------

## 🧰 Rodando Localmente (Sem Docker)

### Instalar uv

``` bash
pip install uv
```

### Instalar dependências

``` bash
uv pip install --system .
```

### Rodar aplicação

``` bash
python main.py
```

Configure variáveis:

``` bash
export ANISETTE_URL=http://localhost:6969
export APPLE_ID=seu_email@apple.com
export APPLE_PWD=sua_senha
```

------------------------------------------------------------------------

## 🧯 Troubleshooting

Ver logs:

``` bash
docker compose logs -f
```

Reiniciar serviço:

``` bash
docker compose restart aura-worker
```

Parar tudo:

``` bash
docker compose down
```