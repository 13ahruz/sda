from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TeamMemberBase(BaseModel):
    full_name: str
    role: Optional[str] = None
    photo_url: Optional[str] = None

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMemberUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    photo_url: Optional[str] = None

class TeamMemberRead(TeamMemberBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TeamSectionItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    photo_url: Optional[str] = None
    button_text: Optional[str] = None
    order: int = 0

class TeamSectionItemCreate(TeamSectionItemBase):
    pass

class TeamSectionItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    photo_url: Optional[str] = None
    button_text: Optional[str] = None
    order: Optional[int] = None

class TeamSectionItemRead(TeamSectionItemBase):
    id: int
    team_section_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TeamSectionBase(BaseModel):
    title: str
    button_text: Optional[str] = None

class TeamSectionCreate(TeamSectionBase):
    items: Optional[List[TeamSectionItemCreate]] = None

class TeamSectionUpdate(BaseModel):
    title: Optional[str] = None
    button_text: Optional[str] = None
    items: Optional[List[TeamSectionItemCreate]] = None

class TeamSectionRead(TeamSectionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    items: List[TeamSectionItemRead] = []
    
    class Config:
        from_attributes = True
