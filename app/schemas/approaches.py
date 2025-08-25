from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ApproachBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 0

class ApproachCreate(ApproachBase):
    pass

class ApproachUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

class ApproachRead(ApproachBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
