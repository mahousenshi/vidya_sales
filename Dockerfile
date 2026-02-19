# 1. Usar uma imagem base oficial do Python (versão slim para ser mais leve)
FROM python:3.10-slim

# 2. Configurar variáveis de ambiente para o Python
# PYTHONDONTWRITEBYTECODE: Evita que o Python escreva arquivos .pyc
# PYTHONUNBUFFERED: Garante que os logs apareçam em tempo real no console
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 4. Instalar dependências do sistema necessárias para o driver do Postgres (psycopg2)
# O Render e outros Linux precisam dessas libs para compilar o driver
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiar o arquivo de requisitos e instalar as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar todo o código do projeto para dentro do container
COPY . .

# 7. Dar permissão de execução para o script de inicialização
# Isso é vital para que o Render consiga rodar o seed e o app
RUN chmod +x start.sh

# 8. Expor a porta 8000 (apenas como documentação, o Render usa a variável $PORT)
EXPOSE 8000

# 9. Comando final que inicia o processo
# Usamos o start.sh que criamos para rodar o seed.py antes do uvicorn
CMD ["./start.sh"]
