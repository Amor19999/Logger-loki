from app import views
from aiohttp import web

async def get_filtered_logs(request):
    # Отримуємо сховище з app
    storage = request.app['storage']
    
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
    app.router.add_route('OPTIONS', '/v1.0/public/log', views.LogCollectionOptions)
    app.router.add_route('POST', '/v1.0/public/log', views.LogCreate)
    app.router.add_route('GET', '/v1.0/public/log', get_filtered_logs)  # Фільтрація
    
    app.router.add_route('GET', '/v1.0/public/log/{id}', views.LogDetail)  # Отримання по ID
    
    app.router.add_route('OPTIONS', '/v1.0/internal/pageview', views.PageViewList)
    app.router.add_route('GET', '/v1.0/internal/pageview', views.PageViewList)
    app.router.add_route('OPTIONS', '/v1.0/public/pageview', views.PageViewList)
    app.router.add_route('POST', '/v1.0/public/pageview', views.PageViewCreate)
