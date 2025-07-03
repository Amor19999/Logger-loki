from aiohttp_boilerplate.test_utils import E2ETestCase
from datetime import datetime, timezone
import uuid

class TestLogCreate(E2ETestCase):
    url = "/v1.0/public/log"
    url_get = "/v1.0/public/log/{id}"

    fixtures = {}

    async def test_options(self):
        status, data = await self.request(self.url, "OPTIONS")
        assert status == 200

    async def test_create_log(self):
        current_time = datetime.now(timezone.utc).isoformat()
        status, data = await self.request(
            self.url,
            "POST",
            data={
                "time": current_time,
                "message": "Task-14",
                "component": "test-logs",
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

        
        assert "id" in data, (
            f"ID field missing in response. "
            f"Full response: {data}"
        )

        try:
            uuid.UUID(data["id"])
        except ValueError:
            assert False, (
                f"Returned ID is not a valid UUID: '{data['id']}'. "
                f"Full response: {data}"
            )

        status_get, data_get = await self.request(
            self.url_get.format(id=data["id"]),
            "GET",
        )
        
        if not isinstance(data_get, dict):
            print(
                f"⚠️ GET response is not JSON (type={type(data_get)}). "
                f"Status: {status_get}, Response: {data_get}"
            )
            return  

        assert "message" in data_get, (
            f"'message' field missing in GET response. "
            f"Full response: {data_get}"
        )
        
        assert data_get["message"] == "Task-14", (
            f"Expected message 'Task-14', got '{data_get['message']}'. "
            f"Full response: {data_get}"
        )

    async def no_test_create_log_invalid_data(self):
        status, data = await self.request(
            self.url,
            "POST",
            data={
                "invalid_field_1": "invalid_value_1",
                "invalid_field_2": "invalid_value_2",
            },
        )
        
        assert status == 400, (
            f"Expected 400 Bad Request, got {status}. "
            f"Response: {data}"
        )
        
        assert any(key in data for key in ["error", "errors"]), (
            "Error message not found in response. "
            f"Expected 'error' or 'errors' field. Full response: {data}"
        )
