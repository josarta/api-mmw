
from fastapi import HTTPException, Request , status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from config.logger import logger , data , genericLoadRequest 
from aiobreaker.state import CircuitBreakerError

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """Function implemented as a parallel application for exception handling

        Args:
            request (Request): _description_
            call_next (_type_): request for entry that failed

        Returns:
            JSONResponse: returns json, captures the exception in the http code message and creates a log
        """
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
        except CircuitBreakerError as e:
            print(e)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal Server Error", "message": "CircuitBreakerError.", "code":-20005},
            )