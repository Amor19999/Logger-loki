from pydantic import BaseModel, validator
from datetime import datetime, timezone
from typing import Optional

class PageviewRequest(BaseModel):
    user_id: str
    page_url: str
    timestamp: datetime
    session_id: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None

    @validator('timestamp', pre=True)
    def convert_to_utc(cls, value):
        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.replace(tzinfo=timezone.utc)
            return value.astimezone(timezone.utc)
        return value

class AnalyticsRequest(BaseModel):
    start: datetime
    end: datetime
    group_by: str = "day"  # day, week, month

    @validator('start', 'end', pre=True)
    def convert_to_utc(cls, value):
        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.replace(tzinfo=timezone.utc)
            return value.astimezone(timezone.utc)
        return value