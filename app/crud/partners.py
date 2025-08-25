from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc
from ..crud.base import CRUDBase
from ..models.partners import Partner, PartnerLogo
from ..schemas.partners import PartnerCreate, PartnerUpdate, PartnerLogoCreate, PartnerLogoUpdate

class CRUDPartner(CRUDBase[Partner, PartnerCreate, PartnerUpdate]):
    def create(self, db: Session, *, obj_in: PartnerCreate) -> Partner:
        # Extract logos data before creating the partner
        obj_in_data = obj_in.model_dump()
        logos_data = obj_in_data.pop('logos', [])
        
        # Create the partner without logos
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # Add logos if any
        if logos_data:
            for logo_data in logos_data:
                logo_obj = PartnerLogo(partner_id=db_obj.id, **logo_data)
                db.add(logo_obj)
            db.commit()
            db.refresh(db_obj)
        
        return db_obj

class CRUDPartnerLogo(CRUDBase[PartnerLogo, PartnerLogoCreate, PartnerLogoUpdate]):
    def get_by_partner(
        self, db: Session, *, partner_id: int, skip: int = 0, limit: int = 100
    ) -> List[PartnerLogo]:
        return (
            db.query(self.model)
            .filter(self.model.partner_id == partner_id)
            .order_by(asc(self.model.order), asc(self.model.id))
            .offset(skip)
            .limit(limit)
            .all()
        )

partner = CRUDPartner(Partner)
partner_logo = CRUDPartnerLogo(PartnerLogo)
