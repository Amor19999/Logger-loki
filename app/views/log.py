from aiohttp_boilerplate.views.retrieve import RetrieveView
from aiohttp_boilerplate.views.create import CreateView

from app import schemas

class LogDetail(RetrieveView):
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


class LogCreate(CreateView):
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
