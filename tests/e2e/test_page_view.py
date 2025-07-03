from aiohttp_boilerplate.test_utils import E2ETestCase
from datetime import datetime, timezone, timedelta
import uuid

class TestPageView(E2ETestCase):  # Змінено назву класу
    url = "/v1.0/public/pageview"  # Оновлено URL для PageView
    url_get = "/v1.0/public/pageview/{id}"

    fixtures = {}

    async def test_options(self):
        status, data = await self.request(self.url, "OPTIONS")
        assert status == 200

    async def test_create(self):  # Змінено назву методу
        current_time = datetime.now(timezone.utc).isoformat()
        status, data = await self.request(
            self.url,
            "POST",
            data={
                "time": current_time,
                "httpRequest": {  # Змінено дані на HTTP-заголовки
                    "method": "GET",
                    "url": "/index.html",
                    "path": "/index.html",
                    "host": "www.example.com",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "acceptLanguage": "en-US,en;q=0.9",
                    "acceptEncoding": "gzip, deflate, br",
                    "connection": "keep-alive",
                    "upgradeInsecureRequests": "1",
                    "ifModifiedSince": "Tue, 01 Jan 2025 10:00:00 GMT",
                    "cacheControl": "max-age=0"
                },
            },
        )

        assert status == 201, print(data)
        assert "id" in data, print(data)

        try:
            uuid.UUID(data["id"])
        except ValueError:
            assert False, (
                f"Returned ID is not a valid UUID: '{data['id']}'"
            )

        status_get, data_get = await self.request(
            self.url_get.format(id=data["id"]),
            "GET",
        )

        assert status_get == 200, print(data_get)
        assert data_get["id"] == data["id"], print(data_get)
        # Перевірка конкретного поля
        assert data_get["httpRequest"]["url"] == "/index.html", print(data_get)

    async def test_filter_pageviews_by_date_range(self):  # Фільтрація за датою
        date_from = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        date_to = datetime.now(timezone.utc).isoformat()

        status, data = await self.request(
            f"{self.url}?date_from={date_from}&date_to={date_to}",
            "GET"
        )

        assert status == 200, f"Expected 200 OK, got {status}. Response: {data}"

        for pageview in data:
            assert date_from <= pageview["time"] <= date_to, (
                f"Pageview time {pageview['time']} is outside filter range {date_from} - {date_to}"
            )

    async def test_filter_pageviews_by_time(self):  # Фільтрація за часом
        time_filter = datetime.now(timezone.utc).isoformat()
        status, data = await self.request(
            f"{self.url}?time={time_filter}",
            "GET"
        )

        assert status == 200, f"Expected 200 OK, got {status}. Response: {data}"

        for pageview in data:
            assert pageview["time"] == time_filter, (
                f"Pageview time {pageview['time']} doesn't match filter {time_filter}"
            )
