from aiohttp_boilerplate.test_utils import E2ETestCase


class TestCreateLog(E2ETestCase):
    url = "/v1.0/public/log"
    url_get = "/v1.0/public/log/{id}"

    fixtures = {}

    # Make sure OPTIONS request working fine
    async def test_options(self):
        status, data = await self.request(
            self.url,
            "OPTIONS",
        )

        assert status == 200

    async def test_create_log(self):
        status, data = await self.request(
            self.url,
            "POST",
            data={
                "time": "2025-06-30T17:01:23Z",
                "message": "Task-14",
                "component": "analytics-api",
                "serviceContext": {
                    "httpRequest": {
                        "method": "POST",
                        "url": "/v1.0/public/log",
                        "userAgent": "Python/3.13 aiohttp/3.11.7",
                        "referer": "",
                        "remoteIp": "127.0.0.1",
                        "protocol": "http",
                    },
                    "user": None,
                    "request_id": "ca789ad6d1984586b04ef867726fd680",
                    "service_name": "analytics-api",
                },
            },
        )

        assert status == 201, print(data)
        assert "id" in data, print(data)

        status, data = await self.request(
            self.url_get.format(id=data["id"]),
            "GET",
        )
        assert data["message"] == "Task-14", print(data)

    async def no_test_create_log_invalid_data(self):
        """
        тут ми навмисно відправляємо не вірні данні
        щоб подивитись що наша система відасть вірну помилку
        """
        status, data = await self.request(
            self.url,
            "POST",
            data={
                "погані данні 1": "погані данні 1",
                "погані данні 2": "погані данні 1",
            },
        )

        assert status == 400, print(data)
        assert data == {"погані данні 1": ["Not a valid integer."]}
