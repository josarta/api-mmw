
from fastapi import HTTPException, Request , status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from config.logger import logger , data , genericLoadRequest 

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as http_exception:
            genericLoadRequest(request)
            data['status_code'] = http_exception.status_code
            logger.info(f"Request receivet at {request.url}" , extra=data)
            return JSONResponse(
                status_code=http_exception.status_code,
                content={"error": "Client Error", "message": str(http_exception.detail)},
            )
        except Exception as e:
           genericLoadRequest(request)
           print(e)
           data['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
           logger.error(f"Request receivet at {request.url}" , extra=data)
           return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal Server Error", "message": "An unexpected error occurred."},
            )