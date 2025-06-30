from aiohttp_boilerplate.dbpool import pg
from aiohttp_boilerplate import sql
from app.services.loki_storage import LokiStorage, create_pool_fix

pg.create_pool = create_pool_fix
sql.SQL = LokiStorage
