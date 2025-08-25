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
    def create(self, db: Session, *, obj_in: AboutCreate) -> About:
        # Extract logos data before creating the about
        obj_in_data = obj_in.model_dump()
        logos_data = obj_in_data.pop('logos', [])
        
        # Create the about without logos
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Add logos if any
        if logos_data:
            for logo_data in logos_data:
                logo_obj = AboutLogo(about_id=db_obj.id, **logo_data)
                db.add(logo_obj)
            db.commit()
            db.refresh(db_obj)
        
        return db_obj

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
