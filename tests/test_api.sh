#!/bin/bash

# Test tracking a pageview (UTC time)
curl -X POST http://localhost:8000/api/v1/track/pageview \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "page_url": "/products/shoes",
    "timestamp": "2023-10-26T14:00:00Z"
  }'

# Test analytics (UTC time range)
curl "http://localhost:8000/api/v1/analytics/pageviews?start=2023-10-20T00:00:00Z&end=2023-10-27T23:59:59Z"
