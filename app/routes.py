from app import views


# Setup routers for our cms app
def setup_routes(app):
    app.router.add_route('OPTIONS', '/v1.0/public/log', views.LogDetail)
    app.router.add_route('GET', '/v1.0/internal/log/{id}', views.LogDetail)
    app.router.add_route('POST', '/v1.0/public/log', views.LogCreate)

    # PageView List
    app.router.add_route('OPTIONS', '/v1.0/internal/pageview', views.PageViewList)
    app.router.add_route('GET', '/v1.0/internal/pageview', views.PageViewList)

    # PageView Create
    app.router.add_route('OPTIONS', '/v1.0/public/pageview', views.PageViewList)
    app.router.add_route('POST', '/v1.0/public/pageview', views.PageViewCreate)
