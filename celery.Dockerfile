FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY .env .



ENV rabbitmq_uri: amqp://rabbitmq:5672


WORKDIR /app/app/
CMD celery -A tasks worker worker --loglevel=info