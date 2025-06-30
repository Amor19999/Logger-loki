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
    def __init__(self, url, log=None):
        self.url = url
        self.query = ''
        self.params = {}
        self.log = log
        if self.log:
            self.log.debug(f"Initialized LokiStorage with URL: {url}")

    async def close(self):
        pass

    async def _send_to_loki(self, data: dict) -> bool:
        """Внутрішній метод для відправки даних у Loki"""
        # Кастомний серіалізатор для datetime
        def json_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")
        
        # Формуємо payload для Loki
        payload = {
            "streams": [{
                "stream": {"service": "analytics-api"},
                "values": [[
                    str(int(datetime.utcnow().timestamp() * 1e9)),  # наносекунди
                    json.dumps(data, default=json_serializer)
                ]]
            }]
        }

        headers = {
            "Content-Type": "application/json",
            "X-Scope-OrgID": "fake"  # Обов'язковий заголовок для Loki
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url,
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status in (200, 201, 204):
                        return True
                    err = await response.text()
                    if self.log:
                        self.log.error('Loki error', f"Status: {response.status}, Error: {err}")
                    # Відразу після логування кидаємо exception з текстом помилки
                    raise LokiException(f"Loki error: Status {response.status}, Error: {err}")
        except Exception as e:
            if self.log:
                self.log.error('Loki connection failed', str(e))
            raise  # Прокидуємо далі для явного фейлу

    async def select(self,
        fields='*', where='', order='', limit='', offset=None, params=None, many=False
    ):
        params = params or {}

        if type(params) is not dict:
            raise LokiException('params have to be dict')

        self.params = {}
        self.params.update(params)
        self.query = 'select {} '.format(fields)  # nosec

        if where:
            self.query += ' where {} {}'.format(where, params)

        if order:
            self.query += ' order by {}'.format(order)

        if limit:
            self.query += ' limit {}'.format(limit)

        if offset is not None:
            self.query += f' offset {offset}'

        self.log.debug('sql query', f'{self.query}', extra={"sql_type": "select"})

        print("query to loki")
        result = ["123"]
        # ToDo
        # Make query to the loki
        # result = await stmt.fetch(*self.params.values())
        return result


    async def insert(self, data: dict) -> dict:
        """Зберігає дані у Loki та повертає унікальний ID"""
        # Генеруємо унікальний ID
        insert_id = str(uuid.uuid4())
        data_with_id = {**data, "id": insert_id}

        if self.log:
            self.log.debug(f"Inserting data to Loki: {data_with_id}")

        # Відправляємо дані до Loki
        if await self._send_to_loki(data_with_id):
            return {"id": insert_id}
        else:
            raise LokiException("Failed to insert data to Loki")

    async def update(self, where: str, params: dict, data: dict) -> int:
        raise LokiException('Not supported')

    async def delete(self, where: str, params: dict) -> int:
        raise LokiException('Not supported')