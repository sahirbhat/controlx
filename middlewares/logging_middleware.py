import time
import logging
from fastapi import Request
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("controlx.log")
    ]
)
logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"REQUEST  | {request.method} {request.url.path} | IP: {request.client.host}")
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    logger.info(f"RESPONSE | {request.method} {request.url.path} | Status: {response.status_code} | Duration: {duration:.2f}ms")
    return response