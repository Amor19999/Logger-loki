# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install fastapi uvicorn python-dotenv logging-loki pydantic

EXPOSE 8000

CMD ["uvicorn", "factum_logger.api:app", "--host", "0.0.0.0", "--port", "8000"]