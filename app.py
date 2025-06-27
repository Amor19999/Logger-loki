from fastapi import FastAPI
from api import router as api_router
from services.db import init_db
from contextlib import asynccontextmanager
import os
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Set UTC timezone for application
    os.environ['TZ'] = 'UTC'
    time.tzset()
    
    # Initialize database
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)