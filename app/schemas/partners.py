from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class PartnerLogoBase(BaseModel):
    image_url: str
    order: int = 0

class PartnerLogoCreate(PartnerLogoBase):
    pass

class PartnerLogoUpdate(BaseModel):
    image_url: Optional[str] = None
    order: Optional[int] = None

class PartnerLogoRead(PartnerLogoBase):
    id: int
    partner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PartnerBase(BaseModel):
    title: str
    button_text: Optional[str] = None

class PartnerCreate(PartnerBase):
    logos: Optional[List[PartnerLogoCreate]] = None

class PartnerUpdate(BaseModel):
    title: Optional[str] = None
    button_text: Optional[str] = None
    logos: Optional[List[PartnerLogoCreate]] = None

class PartnerRead(PartnerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    logos: List[PartnerLogoRead] = []
    
    class Config:
        from_attributes = True
