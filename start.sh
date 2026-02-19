#!/bin/bash

# Rodar o script de seed
echo "===> Rodando Seed de dados..."
python seed.py

# Iniciar o Uvicorn usando a porta definida pelo Render ou 8000 como padrão
echo "===> Iniciando servidor FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
