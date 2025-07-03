from datetime import datetime
from aiohttp_boilerplate.views.list import ListView
from aiohttp_boilerplate.views.create import CreateView
from aiohttp_boilerplate.views.retrieve import RetrieveView

from app import schemas

# class PageViewModel:
#     data = {}

#     def __init__(self, *args, **kwargs):
#         pass

class PageViewDetail(RetrieveView):
    async def _get(self):
        storage = self.request.app.db_pool
        pageview_id = self.request.match_info.get('id')
        obj = await storage.get_log(pageview_id)
        return obj

class PageViewModel:
    def __init__(self, *args, **kwargs):
        self.data = []

class PageViewList(ListView):
    async def perform_get(self, **kwargs):
        storage = self.request.app.db_pool
        filters = {}
        for key, value in kwargs.items():
            if key.endswith(("_from", "_to")) and value:
                try:
                    value = datetime.fromisoformat(value)
                except ValueError:
                    pass
            filters[key] = value
        self.objects = PageViewModel()
        self.objects.data = await storage.select(**filters)

    async def get_data(self, objects):
        return objects.data

    async def perform_get_count(self, where, params):
        return len(self.objects.data)

    def get_model(self):
        return PageViewModel


# class PageViewList(ListView):
#     async def perform_get(self, **kwargs):
#         storage = self.request.app.db_pool
#         filters = {}
#         for key, value in kwargs.items():
#             if key.endswith(("_from", "_to")) and value:
#                 try:
#                     value = datetime.fromisoformat(value)
#                 except ValueError:
#                     pass
#             filters[key] = value
#         self.objects = await storage.select(**filters)

#     async def get_data(self, objects):
#         return objects.data

#     def get_model(self):
#         return PageViewModel


    # async def perform_get(self, **kwargs):
    #     # storage = self.request.app.db_pool
    #     storage = self.request.app.db_pool
    #     pageview_id = self.request.match_info.get('id')
    #     obj = await storage.get_log(pageview_id)
    #     self.objects = PageViewModel()
    #     # self.objects.data = await storage.select(**filters)
        
    #     # Обробка параметрів фільтрації
    #     filters = {}
    #     for key, value in kwargs.items():
    #         if key.endswith(("_from", "_to")) and value:
    #             try:
    #                 value = datetime.fromisoformat(value)
    #             except ValueError:
    #                 pass
    #         filters[key] = value

    #     # Отримання даних
    #     self.objects = PageViewModel()
    #     self.objects.data = await storage.select(**filters)

class PageViewCreate(CreateView):
    def get_model(self):
        return None

    def get_schema(self):
        return schemas.PageViewCreate

    async def perform_create(self, data):
            storage = self.request.app.db_pool
            self.obj = await storage.insert(data)
            return self.obj

    async def get_data(self, obj) -> dict:
        ''' Return id of the object '''
        return {'id': obj["id"]}
