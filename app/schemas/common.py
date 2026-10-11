from pydantic import BaseModel
from typing import Dict, Any, Optional

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
