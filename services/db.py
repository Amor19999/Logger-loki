import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import TIMESTAMP

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://user:password@postgres:5432/analytics')

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class Pageview(Base):
    __tablename__ = 'pageviews'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    page_url = Column(String)
    timestamp = Column(TIMESTAMP(timezone=True), default=func.now(), index=True)
    session_id = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    referrer = Column(String, nullable=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)