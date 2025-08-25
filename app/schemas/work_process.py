from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WorkProcessBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 0
    image_url: Optional[str] = None

class WorkProcessCreate(WorkProcessBase):
    pass

class WorkProcessUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    image_url: Optional[str] = None

class WorkProcessRead(WorkProcessBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
