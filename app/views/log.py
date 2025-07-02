from aiohttp_boilerplate.views.retrieve import RetrieveView
from aiohttp_boilerplate.views.create import CreateView
from aiohttp import web
from app import schemas

async def LogCollectionOptions(request):
    return web.Response(status=204)

# async def post(self):
#     try:
#         raw_data = await self.request.json()
#         schema = self.get_schema()
#         validated_data = schema().load(raw_data)
#         # ... інший код ...
#     except ValidationError as e:
#         return web.json_response({"error": e.messages}, status=400)

# class LogDetail(RetrieveView):
#     # def get_model(self):
#     #     return models.Offer

#     def get_schema(self):
#         return schemas.LogDetail

#     async def before_get(self):
#         self.where = "t0.status={published} and entity_id!=''"

#     async def get_data(self, objects):
#         data = await super().get_data(objects)
#         data = self.schema().dump(obj=data, many=True)

#         return data
class LogDetail(RetrieveView):
    def __init__(self, request):
        super().__init__(request)
        self.obj = None  # Ініціалізувати obj
        
    # async def _get(self):
    #     # Логіка отримання об'єкту
    #     self.obj = await storage.get_log(...)
    #     return self.obj
    async def _get(self):
        storage = self.request.app['storage']
        log_id = self.request.match_info.get('id')
        self.obj = await storage.get_log(log_id)
        return self.obj


class LogCreate(CreateView):
    def get_schema(self):
        return schemas.LogCreate

    # async def post(self):
    #     # Отримуємо "сирі" дані з тіла запиту
    #     raw_data = await self.request.json()
        
    #     # Валідуємо дані за схемою
    #     schema = self.get_schema()
    #     validated_data = schema().load(raw_data)
        
    #     # Виконуємо створення запису
    #     result = await self.perform_create(validated_data)
        
    #     # Форматуємо відповідь
    #     response_data = await self.get_data(result)
    #     return web.json_response(response_data, status=201)

    async def perform_create(self, data: dict):
        res = await self.request.app.db_pool.insert(data)
        return res

    async def get_data(self, obj) -> dict:
        return obj

    async def perform_create(self, data):
        storage = self.request.app['storage']
        return await storage.insert(data)
# class LogCreate(CreateView):
#     # def get_model(self):
#     #     return models.Offer

#     def get_schema(self):
#         return schemas.LogCreate

#     async def before_get(self):
#         self.where = "t0.status={published} and entity_id!=''"

#     async def perform_create(self, data: dict):
#         res = await self.request.app.db_pool.insert(data)
#         return res

#     async def get_data(self, obj) -> dict:
#         return obj
    async def perform_create(self, data: dict):
        self.request.app.logger.debug(f"Saving to Loki: {data}")
        res = await self.request.app.db_pool.insert(data)
        self.request.app.logger.debug(f"Loki response: {res}")
        return res
