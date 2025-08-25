from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AboutLogoBase(BaseModel):
    image_url: str
    order: int = 0

class AboutLogoCreate(AboutLogoBase):
    pass

class AboutLogoUpdate(BaseModel):
    image_url: Optional[str] = None
    order: Optional[int] = None

class AboutLogoRead(AboutLogoBase):
    id: int
    about_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AboutBase(BaseModel):
    experience: str
    project_count: str
    members: str

class AboutCreate(AboutBase):
    logos: Optional[List[AboutLogoCreate]] = None

class AboutUpdate(BaseModel):
    experience: Optional[str] = None
    project_count: Optional[str] = None
    members: Optional[str] = None
    logos: Optional[List[AboutLogoCreate]] = None

class AboutRead(AboutBase):
    id: int
    created_at: datetime
    updated_at: datetime
    logos: List[AboutLogoRead] = []
    
    class Config:
        from_attributes = True
