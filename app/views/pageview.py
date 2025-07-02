from aiohttp_boilerplate.views.list import ListView
from aiohttp_boilerplate.views.create import CreateView

from app import schemas

class PageViewModel:
    data = {}

    def __init__(self, *args, **kwargs):
        pass

class PageViewList(ListView):
    async def perform_get_count(self, where, params):
        return len(self.objects.data)

    async def perform_get(self, **kwargs):
        storage = self.request.app.db_pool
        
        # Обробка параметрів фільтрації
        filters = {}
        for key, value in kwargs.items():
            if key.endswith(("_from", "_to")) and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    pass
            filters[key] = value

        # Отримання даних
        self.objects = PageViewModel()
        self.objects.data = await storage.select(**filters)

    def get_model(self):
        return PageViewModel

class PageViewCreate(CreateView):
    def get_model(self):
        return None

    def get_schema(self):
        return schemas.PageViewCreate

    async def perform_create(self, data):
        storage = self.request.app.db_pool
        return await storage.insert(data)
    
# class PageViewCreate(CreateView):
#     def get_model(self):
#         return None 
    
#     def get_schema(self):
#         return schemas.LogDetail

#     async def before_get(self):
#         self.where = "t0.status={published} and entity_id!=''"

#     async def get_data(self, objects):
#         data = await super().get_data(objects)
#         data = self.schema().dump(obj=data, many=True)

#         return data

#     async def perform_get(self, fields="", **kwargs):
#             self.log.debug("Perform get request" f"fields={fields}, kwargs: {kwargs}")
#             print(fields, kwargs)
#             raw_data = await self.objects.sql.select(
#                 fields=fields, many=True, **kwargs
#             )
#             self.objects = raw_data

#     def get_schema(self):
#         return schemas.PageViewCreate

#     async def perform_create(self, data):
#         storage = self.request.app['storage']
#         return await storage.create_pageview(data)
