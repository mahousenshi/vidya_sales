# 📊 Vidya Analytics Dashboard

Um sistema de monitoramento de vendas que integra dois tipos de bancos de dados para máxima performance: **PostgreSQL** para dados estruturados (vendas) e **MongoDB Atlas** para dados não estruturados (comentários).

## 🚀 Tecnologias Utilizadas

* **Backend:** FastAPI
* **SQL Database:** PostgreSQL 
* **NoSQL Database:** MongoDB Atlas
* **ORM/ODM:** SQLAlchemy e PyMongo
* **Containerização:** Docker & Docker Compose
* **Deploy:** Render

## 🏗️ Arquitetura de Dados

O projeto utiliza uma arquitetura de banco de dados poliglota:
- **Relacional (SQL):** Gerencia a integridade das vendas.
- **Não-Relacional (NoSQL):** Oferece flexibilidade para comentários e feedbacks, permitindo crescimento sem esquemas rígidos.

## 🛠️ Como rodar o projeto localmente

1. **Clone o repositório:**

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```
   
2. **Configure as variáveis de ambiente:**

Crie um arquivo .env na raiz do projeto com as seguintes chaves:

'''python
DATABASE_URL=postgresql://usuario:senha@localhost:5432/vidya_db
MONGO_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/vidya_analytics
'''

3. Inicie com Docker:
    
'''Bash
docker-compose up --build
'''

O sistema irá automaticamente rodar o seed.py para popular os bancos caso estejam vazios.

🌐 Endpoints Principais

'GET /': Mensagem de boas-vindas e status da API.

'GET /api/sales/': Lista todas as vendas.

'POST /api/sales/': Cria uma nova venda.

'GET /api/sales/search?q=': Procura venda com o comentario.

'GET /api/sales/total_revenue': Retorna o total de feito com todas as vendas.

'GET /api/sales/quantity_categories': Retorna a quantidade vendida por categoria.

'GET /api/sales/quantity_products': Retorna a quantidade vendida por produto.

'GET /docs': Documentação interativa Swagger UI.

Desenvolvido por Fabio Ortolan
