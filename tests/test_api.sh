#!/bin/bash

# Тест відстеження переглядів
curl -X POST http://localhost:8000/api/v1/track/pageview \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "page_url": "/products/shoes",
    "timestamp": "2023-10-26T14:00:00Z"
  }'

# Тест аналітики
curl "http://localhost:8000/api/v1/analytics/pageviews?start=2023-10-20T00:00:00Z&end=2023-10-27T23:59:59Z"
