from aiohttp_boilerplate.views.list import ListView
from aiohttp_boilerplate.views.create import CreateView

from app import schemas


class PageViewList(ListView):
    # def get_model(self):
    #     return models.Offer

    def get_schema(self):
        return schemas.PageViewList

    async def before_get(self):
        self.where = "t0.status={published} and entity_id!=''"

    async def get_data(self, objects):
        data = await super().get_data(objects)
        data = self.schema().dump(obj=data, many=True)

        return data

class PageViewCreate(CreateView):
    # def get_model(self):
    #     return models.Offer

    def get_schema(self):
        return schemas.LogDetail

    async def before_get(self):
        self.where = "t0.status={published} and entity_id!=''"

    async def get_data(self, objects):
        data = await super().get_data(objects)
        data = self.schema().dump(obj=data, many=True)

        return data
