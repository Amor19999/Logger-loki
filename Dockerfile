# # Dockerfile
# FROM python:3.11-slim

# WORKDIR /app

# COPY . .

# RUN pip install --upgrade pip && \
#     pip install fastapi uvicorn python-dotenv pydantic python-logging-loki

# EXPOSE 8000

# CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]