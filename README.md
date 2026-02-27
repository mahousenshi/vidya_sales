# 📊 Vidya Analytics Dashboard

Um sistema de monitoramento de vendas que integra uma arquitetura de banco de dados poliglota para máxima performance: **PostgreSQL** para dados estruturados (vendas) e **MongoDB** para dados não estruturados (comentários e logs).

## 🚀 Tecnologias Utilizadas

* **Framework:** FastAPI
* **SQL Database:** PostgreSQL 
* **NoSQL Database:** MongoDB
* **ORM/ODM:** SQLAlchemy e PyMongo
* **Containerização:** Docker & Docker Compose
* **Deploy:** Render

## 🏗️ Arquitetura de Dados

O projeto utiliza uma estratégia de armazenamento híbrido:

- **Relacional (SQL):** Garante a consistência financeira, cálculos de faturamento e integridade referencial das vendas.
- **Não-Relacional (NoSQL):** Armazena feedbacks e comentários, permitindo a evolução do esquema sem migrações complexas de banco de dados.

## 🛠️ Como rodar o projeto localmente

1. **Clone o repositório:**

```bash
git clone git@github.com/mahousenshi/vidya_sales.git
cd vidya_sales
```
   
2. **Configure as variáveis de ambiente:**

Use como modelo o arquivo `.env.example` na raiz do projeto com as seguintes chaves:

```python
DATABASE_URL=postgresql://usuario:senha@localhost:5432/vidya_db
MONGO_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/vidya_analytics
```

Se quiser crie o `.env` usando

```Bash
cp .env.example .env
```

3. Inicie a infraestrutura de dados:

```Bash
docker compose up -d
```

4. Execute a aplicação:

- Instale as dependências do sistema (Linux/Debian):

```Bash
sudo apt-get update && sudo apt-get install -y libpq-dev gcc
```

- Crie o ambiente virtual e instale as bibliotecas:

```Bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

- Rode o seed (facultativo)

```Bash
python seed.py
```

- Inicie o servidor:

```Bash
uvicorn app.main:app --reload
```

## 🏗️ Estrutura do Projeto

A aplicação segue uma estrutura modular para separar a lógica de banco de dados, modelos e rotas da API:


```
.
├── app/
│   ├── routes/
│   │   ├── sales.py      # Endpoints de API (lógica de negócios e cálculos)
│   │   └── views.py      # Rotas de renderização das páginas (Frontend)
│   ├── database.py       # Configuração e conexão com Postgres e MongoDB
│   ├── main.py           # Inicialização do FastAPI e montagem das rotas
│   ├── models.py         # Definição das tabelas SQL (SQLAlchemy)
│   └── schemas.py        # Modelos de validação de dados (Pydantic)
├── templates/            # Arquivos HTML (Dashboard e Index)
├── seed.py               # Script para população inicial dos bancos de dados
├── docker-compose.yml    # Orquestração de containers localmente
└── requirements.txt      # Dependências do sistema
```

## 🌐 Endpoints Principais

- `GET /`: Mensagem de boas-vindas e status da API.

- `GET /api/sales/`: Lista todas as vendas.

- `POST /api/sales/`: Cria uma nova venda.

- `GET /api/sales/search?q=<termo>`: Procura venda com o comentario.

- `GET /api/sales/total_revenue`: Retorna o total de feito com todas as vendas.

- `GET /api/sales/quantity_categories`: Retorna a quantidade vendida por categoria.

- `GET /api/sales/quantity_products`: Retorna a quantidade vendida por produto.

- `GET /docs`: Documentação interativa Swagger UI.

---

Desenvolvido por Fabio Ortolan
