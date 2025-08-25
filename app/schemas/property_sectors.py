from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class PropertySectorBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 0

class PropertySectorCreate(PropertySectorBase):
    pass

class PropertySectorUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

class SectorInnBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 0

class SectorInnCreate(SectorInnBase):
    property_sector_id: int

class SectorInnUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

class SectorInnRead(SectorInnBase):
    id: int
    property_sector_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PropertySectorRead(PropertySectorBase):
    id: int
    created_at: datetime
    updated_at: datetime
    inns: List[SectorInnRead] = []
    
    class Config:
        from_attributes = True
