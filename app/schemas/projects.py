from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ProjectPhotoBase(BaseModel):
    image_url: str
    order: int = 0

class ProjectPhotoCreate(ProjectPhotoBase):
    pass

class ProjectPhotoUpdate(BaseModel):
    image_url: Optional[str] = None
    order: Optional[int] = None

class ProjectPhotoRead(ProjectPhotoBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    tag: Optional[str] = None
    client: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=2100)
    property_sector_id: Optional[int] = None
    cover_photo_url: Optional[str] = None

class ProjectCreate(ProjectBase):
    photos: Optional[List[ProjectPhotoCreate]] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    tag: Optional[str] = None
    client: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=2100)
    property_sector_id: Optional[int] = None
    cover_photo_url: Optional[str] = None
    photos: Optional[List[ProjectPhotoCreate]] = None

class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    photos: List[ProjectPhotoRead] = []
    
    class Config:
        from_attributes = True
