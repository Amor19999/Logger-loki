# /api_logger.py
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from .core import get_logger, log_structured
from datetime import datetime

app = FastAPI()

class LogStackFrame(BaseModel):
    func: Optional[str]
    source: Optional[str]
    line: Optional[str]

class LogPayload(BaseModel):
    level: str = "info"
    message: str
    service: Optional[str]
    component: Optional[str]
    version: Optional[str]
    repository: Optional[str]
    revision_id: Optional[str]
    msg_id: Optional[str]
    error: Optional[str]
    data: Optional[Dict] = {}
    stack: Optional[List[LogStackFrame]] = []
    caller: Optional[str]
    severity: Optional[str]
    time: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

@app.post("/log")
async def receive_log(payload: LogPayload):
    logger = get_logger(extra_tags={
        "service": payload.service or "frontend",
        "component": payload.component or "unknown",
        "version": payload.version or "unknown",
        "repository": payload.repository or "unknown",
        "level": payload.level,
    })

    log_structured(
        logger,
        level=payload.level,
        message=payload.message,
        service=payload.service,
        component=payload.component,
        version=payload.version,
        repository=payload.repository,
        revision_id=payload.revision_id,
        msg_id=payload.msg_id,
        error=payload.error,
        data=payload.data,
        stack=[frame.dict() for frame in payload.stack],
        caller=payload.caller,
        severity=payload.severity,
        time=payload.time
    )

    return {"status": "ok"}
