# app/views/__init__.py
from .log import LogCreate, LogDetail
from .pageview import PageViewList, PageViewCreate

__all__ = [
    'LogCreate', 'LogDetail',
    'PageViewList', 'PageViewCreate'
]
