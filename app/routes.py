from app.views.log import LogCreate, LogDetail
from app.views.pageview import PageViewList, PageViewCreate
from app.views.pageview import PageViewDetail, PageViewStats


def setup_routes(app):
    app.router.add_route('OPTIONS', '/v1.0/public/log', LogDetail)
    app.router.add_route('POST', '/v1.0/public/log', LogCreate)
    app.router.add_route('GET', '/v1.0/public/log/{id}', LogDetail)
    
    app.router.add_route('GET', '/v1.0/public/pageview/{id}', PageViewDetail)  
    app.router.add_route('OPTIONS', '/v1.0/public/pageview', PageViewDetail)
    app.router.add_route('POST', '/v1.0/public/pageview', PageViewCreate)
    app.router.add_route('GET', '/v1.0/public/pageview', PageViewList)

    app.router.add_route('GET', '/v1.0/internal/pageview_stats', PageViewStats) #add 04.07 for filter date

