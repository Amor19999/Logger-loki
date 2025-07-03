from aiohttp_boilerplate.views.retrieve import RetrieveView
from aiohttp_boilerplate.views.create import CreateView
from app import schemas


class LogDetail(RetrieveView):
    def __init__(self, request):
        super().__init__(request)
        self.obj = None  # Ініціалізувати obj

    # async def _get(self):
    #     # Логіка отримання об'єкту
    #     self.obj = await storage.get_log(...)
    #     return self.obj
    async def _get(self):
        storage = self.request.app.db_pool
        log_id = self.request.match_info.get('id')
        self.obj = await storage.get_log(log_id)
        return self.obj


class LogCreate(CreateView):
    def get_schema(self):
        return schemas.LogCreate

    async def perform_create(self, data: dict):
        self.obj = await self.request.app.db_pool.insert(data)
        return self.obj

    async def get_data(self, obj) -> dict:
        return self.obj
