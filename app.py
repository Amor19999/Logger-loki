from fastapi import FastAPI
from api import router as api_router
from services.db import init_db
import asyncio

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def on_startup():
    await init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
