from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PageviewRequest(BaseModel):
    user_id: str
    page_url: str
    timestamp: datetime
    session_id: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None

class AnalyticsRequest(BaseModel):
    start: datetime
    end: datetime
    group_by: str = "day"  # day, week, month
