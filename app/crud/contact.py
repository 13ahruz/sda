from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..crud.base import CRUDBase
from ..models.contact import ContactMessage
from ..schemas.contact import ContactMessageCreate, ContactMessageUpdate

class CRUDContactMessage(CRUDBase[ContactMessage, ContactMessageCreate, ContactMessageUpdate]):
    def get_multi_ordered(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ContactMessage]:
        """Get contact messages ordered by creation date (newest first)"""
        return (
            db.query(self.model)
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_unread(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ContactMessage]:
        """Get unread contact messages"""
        return (
            db.query(self.model)
            .filter(self.model.is_read == False)
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_status(
        self,
        db: Session,
        *,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[ContactMessage]:
        """Get contact messages by status"""
        return (
            db.query(self.model)
            .filter(self.model.status == status)
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

contact_message = CRUDContactMessage(ContactMessage)
