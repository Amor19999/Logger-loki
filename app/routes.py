from app.views.log import LogCreate, LogDetail, LogCollectionOptions
from app.views.pageview import PageViewList, PageViewCreate
from aiohttp import web

async def get_filtered_logs(request):
    # Отримуємо сховище з app
    storage = request.app['storage']
    # storage = self.request.app['storage']


    # Параметри фільтрації
    params = request.query
    date_from = params.get('date_from')
    date_to = params.get('date_to')
    time_filter = params.get('time')
    
    # Фільтрація даних
    filtered_data = await storage.filter_logs(
        date_from=date_from, 
        date_to=date_to,
        time=time_filter
    )
    return web.json_response(filtered_data)



def setup_routes(app):
    app.router.add_route('OPTIONS', '/v1.0/public/log', LogCollectionOptions)
    app.router.add_route('POST', '/v1.0/public/log', LogCreate)
    app.router.add_route('GET', '/v1.0/public/log', get_filtered_logs)
    app.router.add_route('GET', '/v1.0/public/log/{id}', LogDetail)
    
    app.router.add_route('GET', '/v1.0/public/pageview', PageViewList)
    app.router.add_route('OPTIONS', '/v1.0/internal/pageview', PageViewList)
    app.router.add_route('GET', '/v1.0/internal/pageview', PageViewList)
    app.router.add_route('OPTIONS', '/v1.0/public/pageview', PageViewList)
    app.router.add_route('POST', '/v1.0/public/pageview', PageViewCreate)

