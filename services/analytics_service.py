from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
from .db import AsyncSessionLocal, Pageview
from sqlalchemy import select, func

async def save_pageview(data: dict):
    async with AsyncSessionLocal() as session:
        pageview = Pageview(**data)
        session.add(pageview)
        await session.commit()

async def get_pageviews_analytics(start: datetime, end: datetime, group_by: str = "day"):
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
        labels = [row.period.strftime('%a') for row in rows]
        values = [[1, row.count] for row in rows]
        total = sum(row.count for row in rows)
        return {'labels': labels, 'values': values, 'total': total}


async def save_pageview(data: dict):
    pageviews_storage.append(data)

async def get_pageviews_analytics(start: datetime, end: datetime, group_by: str = "day"):
    # Фільтрація даних за період
    filtered = [p for p in pageviews_storage 
                if start <= p['timestamp'] <= end]
    
    # Групування даних
    grouped = defaultdict(int)
    current = start
    
    # Створення порожніх бакетів для періоду
    while current <= end:
        if group_by == "day":
            key = current.date()
            current += timedelta(days=1)
        elif group_by == "week":
            key = current.isocalendar()[1]  # Номер тижня
            current += timedelta(weeks=1)
        elif group_by == "month":
            key = (current.year, current.month)
            current = (current.replace(day=1) + timedelta(days=32)).replace(day=1)
        else:
            raise ValueError("Invalid group_by value")
        grouped[key] = 0
    
    # Заповнення даними
    for view in filtered:
        if group_by == "day":
            key = view['timestamp'].date()
        elif group_by == "week":
            key = view['timestamp'].isocalendar()[1]
        elif group_by == "month":
            key = (view['timestamp'].year, view['timestamp'].month)
        grouped[key] += 1
    
    # Форматування результату
    labels = []
    values = []
    
    for key in sorted(grouped.keys()):
        if group_by == "day":
            labels.append(key.strftime("%a"))
            values.append([1, grouped[key]])
        elif group_by == "week":
            labels.append(f"Week {key}")
            values.append([1, grouped[key]])
        elif group_by == "month":
            year, month = key
            labels.append(f"{year}-{month:02d}")
            values.append([1, grouped[key]])
    
    total = sum(grouped.values())
    
    return {
        'labels': labels,
        'values': values,
        'total': total
    }
