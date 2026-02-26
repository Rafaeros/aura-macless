# 🚀 Macless Worker

Worker Python responsável por consumir os serviços do Macless Haystack e
Anisette Server para processamento e integração de dados.

<hr/>

## 🏗 Arquitetura

O sistema é composto por 3 containers Docker:

-   anisette → Serviço Anisette
-   macless-haystack → Endpoint do Macless Haystack
-   macless-worker → Este projeto (worker)

Todos rodam na mesma rede Docker.

<hr/>

## 📦 Pré-requisitos

-   Docker
-   Docker Compose (v2+ recomendado)

<hr/>

## 🌐 Rede Docker

Os containers se comunicam através de uma rede interna chamada:

mh-network

⚠ Importante:\
Dentro do container **não utilize localhost** para acessar outros
serviços.

Use os nomes dos containers como hostname:

http://macless-haystack:6176\
http://anisette:6969

<hr/>

## 🐳 Executando com Docker Compose (Recomendado)

Basta rodar:

docker compose up -d --build

Isso irá:

-   Criar a rede automaticamente
-   Subir o Anisette Server
-   Subir o Macless Haystack
-   Subir o Macless Worker

<hr/>

## 🔐 Primeira Configuração do Macless

Na primeira execução, você deve configurar o Apple ID.

Execute em modo interativo:

docker compose run --rm macless-haystack

Será solicitado:

-   Apple ID
-   Senha
-   Código 2FA

Quando aparecer:

serving at port 6176 over HTTP

Interrompa (CTRL+C) e execute:

docker compose up -d

<hr/>

## 🔌 Portas Expostas

  Serviço            Porta
  ------------------ -------
  Anisette Server    6969
  Macless Haystack   6176
  Macless Worker     5000

<hr/>

## 📁 Volumes Persistentes

-   anisette-v3_data → Dados do Anisette
-   mh_data → Dados do Macless

Isso garante que você não precise refazer login no Apple ID a cada
restart.

<hr/>

## 🧪 Desenvolvimento Local

Para rodar apenas o worker:

docker build -t macless-worker . docker run -p 5000:5000 macless-worker

⚠ Nesse caso você precisará apontar para serviços externos manualmente.

<hr/>

## 🔄 Restart Automático

Todos os serviços estão configurados com política de restart automático.

<hr/>

## 🧯 Troubleshooting

Ver logs:

docker compose logs -f

Reiniciar serviço específico:

docker compose restart macless-worker

Parar tudo:

docker compose down

<hr/>
