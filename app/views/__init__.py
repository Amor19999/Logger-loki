# from .log import LogDetail, LogCreate
# from .pageview import PageViewList, PageViewCreate

# __all__ = ('LogDetail', 'LogCreate', 'PageViewList', 'PageViewCreate',)


# app/views/__init__.py
from .log import LogCreate, LogDetail
from .pageview import PageViewList, PageViewCreate

async def LogCollectionOptions(request):
    return web.Response(status=204)

__all__ = [
    'LogCreate', 'LogDetail', 'LogCollectionOptions',
    'PageViewList', 'PageViewCreate'
]
