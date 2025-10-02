from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class NewsSectionBase(BaseModel):
    heading: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    order: int = 0

class NewsSectionCreate(NewsSectionBase):
    pass

class NewsSectionUpdate(BaseModel):
    heading: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None

class NewsSectionRead(NewsSectionBase):
    id: int
    news_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    photo_url: Optional[str] = None
    category: Optional[str] = None  # Trends, Insights, Guides
    tags: List[str] = []
    author: Optional[str] = None
    read_time: Optional[str] = None
    order: int = 0

class NewsCreate(NewsBase):
    sections: Optional[List[NewsSectionCreate]] = None

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    photo_url: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    read_time: Optional[str] = None
    order: Optional[int] = None
    sections: Optional[List[NewsSectionCreate]] = None

class NewsRead(NewsBase):
    id: int
    created_at: datetime
    updated_at: datetime
    sections: List[NewsSectionRead] = []
    
    class Config:
        from_attributes = True
