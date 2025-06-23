# 📝 Logger API

Цей проєкт реалізує HTTP-інтерфейс для прийому структурованих логів з frontend або інших клієнтів, і відправляє їх у **Grafana Loki**. Він базується на FastAPI та використовує `logging-loki`.

---

## 📁 Структура проєкту

```
logger-loki/
│
├── init.py # Ініціалізація пакету
├── api.py # FastAPI роутер з ендпоінтом /log
├── core.py # Логіка форматування та відправки логів
├── logger_dashboard.json # Grafana Dashboard для візуалізації логів
```

---

## 🚀 Можливості

- Прийом POST-запитів з логами
- Підтримка структурованого формату (stacktrace, error, serviceContext тощо)
- Відправка логів до Grafana Loki
- Docker-образ для запуску в production
- Підготовлений Grafana Dashboard (`logger_dashboard.json`)

---

## ⚙️ Установка

### Встановлення з pip

```bash
git clone https://github.com/your-org/factum-logger.git
cd factum-logger
pip install -e .
```

або через setup.py:
```
python setup.py install
```

🐳 Docker
1. Побудова Docker-образу:

```
docker build -t factum-logger .
```

2. Створіть .env файл:

```
LOKI_URL=http://your-loki-host:3100/loki/api/v1/push
APP_NAME=myapp
ENV=stage
```

3. Запуск:

```
docker run -p 8000:8000 --env-file .env factum-logger
```

📡 API
POST /log
Приклад тіла запиту:

```
{
  "message": "EscrowCreateAccount error for 615",
  "error": "validator error",
  "msg_id": "123456",
  "service": "app",
  "version": "20250421:abc123",
  "repository": "wallet-api/i-app",
  "revision_id": "abc123",
  "component": "pubsub",
  "data": {
    "user_id": "42"
  },
  "stack": [
    {"func": "main", "line": "10", "source": "main.py"}
  ],
  "caller": "main.py:10",
  "level": "error"
}
```

📊 Grafana Dashboard

Файл logger_dashboard.json можна імпортувати до Grafana для перегляду логів з фільтрацією за:

    msg_id

    service

    version

    component

    severity

🧪 Тестування

```
curl -X POST http://localhost:8000/log \
  -H "Content-Type: application/json" \
  -d @test_log.json
```

📌 Залежності

    fastapi

    uvicorn

    pydantic

    logging-loki

    python-dotenv