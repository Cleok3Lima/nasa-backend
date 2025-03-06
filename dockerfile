FROM python:3.9

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y netcat-openbsd
RUN pip install --no-cache-dir fastapi[all] uvicorn requests psycopg2 sqlalchemy

CMD ["sh", "./wait-for-db.sh"]
