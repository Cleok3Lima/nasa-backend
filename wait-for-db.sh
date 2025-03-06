#!/bin/sh

echo "Esperando o banco de dados iniciar..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Banco de dados pronto! Iniciando a aplicação..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
