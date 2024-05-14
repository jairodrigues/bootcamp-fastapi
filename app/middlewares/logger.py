from fastapi.responses import JSONResponse
from ..utils.logger import logger
import uuid

async def request_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    with logger.contextualize(request_id=request_id):
        logger.info("Request started")
        try:
            response = await call_next(request)
        except Exception as ex:
            logger.error(f"Request failed: Error {ex}")
            return JSONResponse(content={"success": False}, status_code=500)
        finally:
            response.headers["X-Request-ID"] = request_id
            logger.info(f"Request ended: Status {response.status_code}")
            return response
