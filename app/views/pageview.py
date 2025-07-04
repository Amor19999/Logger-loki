from datetime import datetime
from aiohttp_boilerplate.views.list import ListView
from aiohttp_boilerplate.views.create import CreateView
from aiohttp_boilerplate.views.retrieve import RetrieveView

from app import schemas

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

####################  Add 04.07  #################################
class PageViewStats(ListView):
    def get_schema(self):
        return schemas.PageViewList  # або окрема схема для відповіді

    async def perform_get(self, **kwargs):
        storage = self.request.app.db_pool
        # отримуємо параметри
        event_type = self.request.query.get("type")
        date_from_str = self.request.query.get("date_from")
        date_to_str = self.request.query.get("date_to")
        # перетворюємо у datetime
        date_from = datetime.fromisoformat(date_from_str) if date_from_str else None
        date_to = datetime.fromisoformat(date_to_str) if date_to_str else None
        filters = {}
        if event_type:
            filters["type"] = event_type
        if date_from:
            filters["timestamp_from"] = date_from
        if date_to:
            filters["timestamp_to"] = date_to
        self.objects = PageViewModel()
        self.objects.data = await storage.select(**filters)

    async def get_data(self, objects):
        # групуємо по днях
        stats = {}
        for obj in objects.data:
            dt = obj["timestamp"]
            if isinstance(dt, str):
                dt_obj = datetime.fromisoformat(dt)
            else:
                dt_obj = dt
            day_str = dt_obj.date().isoformat()
            stats[day_str] = stats.get(day_str, 0) + 1
        return stats

    def get_model(self):
        return PageViewModel
