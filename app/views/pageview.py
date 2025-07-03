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
        # storage = self.request.app.db_pool
        storage = self.request.app.db_pool
        self.objects = PageViewModel()
        # self.objects.data = await storage.select(**filters)
        
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
            self.obj = await storage.insert(data)
            return self.obj

    async def get_data(self, obj) -> dict:
        ''' Return id of the object '''
        return {'id': obj["id"]}
