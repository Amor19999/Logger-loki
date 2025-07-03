from aiohttp_boilerplate.logging import gcp_logger
import uuid
import json
import aiohttp
from datetime import datetime


async def create_pool_fix(conf, loop):
    return LokiStorage(conf["database"], gcp_logger.GCPLogger("loki_storage"))

class LokiException(Exception):
    pass

class LokiStorage(object):
    """
    Зберігає логи у Grafana Loki через HTTP API.
    """

    def __init__(self, url, log=None):
        self.url = url
        self.log = log
        self.logs = {}
        if self.log:
            self.log.debug(f"Initialized LokiStorage with URL: {url}")

    @staticmethod
    def _json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='ignore')
        raise TypeError(f"Type {type(obj)} not serializable")

    async def close(self):
        pass

    async def _send_to_loki(self, data: dict) -> bool:
        payload = {
            "streams": [{
                "stream": {"service": "analytics-api"},
                "values": [[
                    str(int(datetime.utcnow().timestamp() * 1e9)),
                    json.dumps(data, default=self._json_serializer)
                ]]
            }]
        }

        headers = {
            "Content-Type": "application/json",
            "X-Scope-OrgID": "fake"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status in (200, 201, 204):
                        return True
                    err = await response.text()
                    if self.log:
                        self.log.error('Loki error', f"Status: {response.status}, Error: {err}")
                    return False
        except Exception as e:
            if self.log:
                self.log.error('Loki connection failed', str(e))
            return False

    async def select(self, fields='*', where='', order='', limit='', offset=None, params=None, many=False):
        if self.log:
            self.log.debug('select is not supported for Loki', extra={"sql_type": "select"})
        return []

    async def insert(self, data: dict) -> dict:
        insert_id = str(uuid.uuid4())
        data_with_id = {**data, "id": insert_id}

        if self.log:
            self.log.debug(f"Inserting data to Loki: {json.dumps(data_with_id, indent=2, default=self._json_serializer)}")

        if await self._send_to_loki(data_with_id):
            self.logs[insert_id] = data_with_id  # Зберігаємо у кеш
            return {"id": insert_id}
            # return {"id": insert_id}
        raise LokiException("Failed to insert data to Loki")
    


    async def update(self, where: str, params: dict, data: dict) -> int:
        raise LokiException('Not supported')

    async def delete(self, where: str, params: dict) -> int:
        raise LokiException('Not supported')


    async def save_log(self, log_data: dict):
        log_id = log_data["id"]
        self.logs[log_id] = log_data  # Збереження логу

    async def get_log(self, log_id: str):
        return self.logs.get(log_id)  # Отримання логу за ID