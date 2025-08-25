from typing import List
from sqlalchemy.orm import Session
from ..crud.base import CRUDBase
from ..models.about import About, AboutLogo
from ..schemas.about import (
    AboutCreate,
    AboutUpdate,
    AboutLogoCreate,
    AboutLogoUpdate
)

class CRUDAbout(CRUDBase[About, AboutCreate, AboutUpdate]):
    def get_multi_ordered(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[About]:
        """Get about sections ordered by display order"""
        return (
            db.query(self.model)
            .order_by(self.model.display_order.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDAboutLogo(CRUDBase[AboutLogo, AboutLogoCreate, AboutLogoUpdate]):
    def get_by_about(
        self,
        db: Session,
        *,
        about_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AboutLogo]:
        """Get logos by about section ID"""
        return (
            db.query(self.model)
            .filter(self.model.about_id == about_id)
            .order_by(self.model.display_order.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

about = CRUDAbout(About)
about_logo = CRUDAboutLogo(AboutLogo)
