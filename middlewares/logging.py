import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("./db/app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()

        logger.info(f"Incoming request: {request.method} {request.url}")

        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            f"Response status: {response.status_code} - Time taken: {process_time:.4f}s"
        )

        return response
