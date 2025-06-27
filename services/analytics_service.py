from datetime import datetime, timezone
from sqlalchemy import select, func
from .db import AsyncSessionLocal, Pageview

async def save_pageview(data: dict):
    async with AsyncSessionLocal() as session:
        pageview = Pageview(**data)
        session.add(pageview)
        await session.commit()

async def get_pageviews_analytics(start: datetime, end: datetime, group_by: str = "day"):
    # Ensure UTC timezone
    start = start.astimezone(timezone.utc)
    end = end.astimezone(timezone.utc)
    
    async with AsyncSessionLocal() as session:
        if group_by == "day":
            trunc = func.date_trunc('day', Pageview.timestamp)
        elif group_by == "week":
            trunc = func.date_trunc('week', Pageview.timestamp)
        elif group_by == "month":
            trunc = func.date_trunc('month', Pageview.timestamp)
        else:
            raise ValueError("Invalid group_by value")

        stmt = (
            select(trunc.label("period"), func.count().label("count"))
            .where(Pageview.timestamp.between(start, end))
            .group_by("period")
            .order_by("period")
        )
        result = await session.execute(stmt)
        rows = result.fetchall()
        
        # Format labels based on group_by
        if group_by == "day":
            labels = [row.period.strftime('%a') for row in rows]
        elif group_by == "week":
            labels = [f"Week {row.period.strftime('%V')}" for row in rows]
        elif group_by == "month":
            labels = [row.period.strftime('%Y-%m') for row in rows]
            
        values = [[1, row.count] for row in rows]
        total = sum(row.count for row in rows)
        
        return {
            'labels': labels,
            'values': values,
            'total': total
        }