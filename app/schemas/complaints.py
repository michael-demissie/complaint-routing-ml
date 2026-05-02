from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ComplaintCreate(BaseModel):
    complaint_text: str

class ComplaintResponse(BaseModel):
    department: Optional[str]
    priority: Optional[str]
