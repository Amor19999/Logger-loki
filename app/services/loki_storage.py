from aiohttp_boilerplate.logging import gcp_logger

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

    async def close(self):
        pass

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
        self.query = 'insert values({}) {}'.format(
            ','.join(data.keys()),
            ','.join(['$%d' % (x + 1) for x in range(0, data.__len__())]),
        )
        self.log.debug('sql query', f'{self.query}', extra={"sql_type": "insert"})

        print("save data to loki")
        result = {"id": "INSERT 1"}
        # ToDo
        # Save data to loki
        # result = await self.conn.fetchrow(self.query, *data.values())

        return result

    async def update(self, where: str, params: dict, data: dict) -> int:
        raise LokiException('Not supported')

    async def delete(self, where: str, params: dict) -> int:
        raise LokiException('Not supported')
