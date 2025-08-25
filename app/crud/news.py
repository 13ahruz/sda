from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, and_, func
from ..crud.base import CRUDBase
from ..models.news import News, NewsSection
from ..schemas.news import NewsCreate, NewsUpdate, NewsSectionCreate, NewsSectionUpdate

class CRUDNews(CRUDBase[News, NewsCreate, NewsUpdate]):
    def get_multi_filtered(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        tags: Optional[List[str]] = None
    ) -> List[News]:
        query = db.query(self.model)
        
        if tags:
            # Filter by any of the provided tags using PostgreSQL array operations
            query = query.filter(self.model.tags.overlap(tags))
            
        return (
            query
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDNewsSection(CRUDBase[NewsSection, NewsSectionCreate, NewsSectionUpdate]):
    def get_by_news(
        self, db: Session, *, news_id: int, skip: int = 0, limit: int = 100
    ) -> List[NewsSection]:
        return (
            db.query(self.model)
            .filter(self.model.news_id == news_id)
            .order_by(asc(self.model.order), asc(self.model.id))
            .offset(skip)
            .limit(limit)
            .all()
        )

news = CRUDNews(News)
news_section = CRUDNewsSection(NewsSection)
