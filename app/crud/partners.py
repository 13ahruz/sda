from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc
from ..crud.base import CRUDBase
from ..models.partners import Partner, PartnerLogo
from ..schemas.partners import PartnerCreate, PartnerUpdate, PartnerLogoCreate, PartnerLogoUpdate

class CRUDPartner(CRUDBase[Partner, PartnerCreate, PartnerUpdate]):
    pass

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
