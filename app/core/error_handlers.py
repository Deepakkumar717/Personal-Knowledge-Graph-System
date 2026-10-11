import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
from app.core.exceptions import AppException

logger = logging.getLogger("knowledge_graph")

def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        formatted_errors = []
        for error in exc.errors():
            loc = " -> ".join(str(l) for l in error.get("loc", []))
            formatted_errors.append({
                "location": loc,
                "msg": error.get("msg"),
                "type": error.get("type"),
            })
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "VALIDATION_ERROR",
                "message": "Input validation failed",
                "details": {"errors": formatted_errors},
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        logger.error(f"Database integrity error: {exc}")
        msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        if "UNIQUE constraint failed" in msg:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "error": "CONFLICT",
                    "message": "A resource with this unique constraint already exists.",
                    "details": {"db_error": msg},
                },
            )
        if "FOREIGN KEY constraint failed" in msg:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "error": "FOREIGN_KEY_VIOLATION",
                    "message": "Referenced resource does not exist.",
                    "details": {"db_error": msg},
                },
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": "INTEGRITY_ERROR",
                "message": "Database constraint violation.",
                "details": {"db_error": msg},
            },
        )

    @app.exception_handler(OperationalError)
    async def operational_error_handler(request: Request, exc: OperationalError):
        logger.error(f"Database operational error: {exc}")
        msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        if "database is locked" in msg.lower() or "busy" in msg.lower():
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={
                    "error": "DATABASE_LOCKED",
                    "message": "Database is currently busy or locked, please retry.",
                    "details": {},
                },
            )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "A database error occurred.",
                "details": {},
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception on {request.method} {request.url.path}: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
                "details": {},
            },
        )
