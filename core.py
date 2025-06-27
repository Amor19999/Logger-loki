# core.py
import logging
import os
import json
from datetime import datetime
from logging_loki import LokiHandler
from dotenv import load_dotenv

load_dotenv()

LOKI_URL = os.getenv("LOKI_URL")
APP_NAME = os.getenv("APP_NAME", "myapp")
ENV = os.getenv("ENV", "stage")

def get_logger(name="main", extra_tags=None):
    base_tags = {
        "app": APP_NAME,
        "env": ENV,
    }
    if extra_tags:
        base_tags.update(extra_tags)

    handler = LokiHandler(
        url=LOKI_URL,
        tags=base_tags,
        version="1",
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    logger.addHandler(handler)
    logger.addHandler(stream_handler)
    return logger

def log_structured(
    logger,
    *,
    level="info",
    message=None,
    service=None,
    component=None,
    version=None,
    repository=None,
    revision_id=None,
    msg_id=None,
    error=None,
    data=None,
    stack=None,
    caller=None,
    severity=None,
    time=None
):
    payload = {
        "time": time or datetime.utcnow().isoformat() + "Z",
        "message": message,
        "severity": severity or level.upper(),
        "error": error,
        "component": component,
        "caller": caller,
        "data": data or {},
        "stack": stack or [],
        "serviceContext": {
            "service": service,
            "version": version,
            "msg_id": msg_id,
            "sourceReference": {
                "repository": repository,
                "revisionId": revision_id,
            } if repository and revision_id else None,
        }
    }

    clean_payload = {k: v for k, v in payload.items() if v is not None}
    if "serviceContext" in clean_payload:
        clean_payload["serviceContext"] = {
            k: v for k, v in clean_payload["serviceContext"].items() if v is not None
        }
        if not clean_payload["serviceContext"]:
            del clean_payload["serviceContext"]

    log_func = getattr(logger, level, logger.info)
    log_func(json.dumps(clean_payload, ensure_ascii=False))