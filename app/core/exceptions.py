from typing import Any, Dict, Optional

class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details or {}
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=404, error_code="NOT_FOUND", message=message, details=details)

class ConflictException(AppException):
    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=409, error_code="CONFLICT", message=message, details=details)

class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=400, error_code="BAD_REQUEST", message=message, details=details)

class ValidationException(AppException):
    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=422, error_code="VALIDATION_ERROR", message=message, details=details)
