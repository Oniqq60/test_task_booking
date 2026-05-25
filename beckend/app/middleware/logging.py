import time
import uuid
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.middleware.logging")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.time()

        logger.info(f"🚀 [{request_id}] {request.method} {request.url.path}")
        if request.query_params:
            logger.debug(f"📦 [{request_id}] Query: {dict(request.query_params)}")

        try:
            response: Response = await call_next(request)
            process_time = time.time() - start_time
            
            logger.info(
                f"✅ [{request_id}] {response.status_code} | {request.method} {request.url.path} | ⏱️ {process_time:.4f}s"
            )
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.exception(
                f"❌ [{request_id}] INTERNAL ERROR: {str(e)} | {request.method} {request.url.path} | ⏱️ {process_time:.4f}s"
            )
            raise