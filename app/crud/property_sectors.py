from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc
from ..crud.base import CRUDBase
from ..models.property_sectors import PropertySector, SectorInn
from ..schemas.property_sectors import PropertySectorCreate, PropertySectorUpdate, SectorInnCreate, SectorInnUpdate

class CRUDPropertySector(CRUDBase[PropertySector, PropertySectorCreate, PropertySectorUpdate]):
    def get_multi_ordered(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[PropertySector]:
        return (
            db.query(self.model)
            .order_by(asc(self.model.order), asc(self.model.id))
            .offset(skip)
            .limit(limit)
            .all()
        )

class CRUDSectorInn(CRUDBase[SectorInn, SectorInnCreate, SectorInnUpdate]):
    def get_by_property_sector(
        self, db: Session, *, property_sector_id: int, skip: int = 0, limit: int = 100
    ) -> List[SectorInn]:
        return (
            db.query(self.model)
            .filter(self.model.property_sector_id == property_sector_id)
            .order_by(asc(self.model.order), asc(self.model.id))
            .offset(skip)
            .limit(limit)
            .all()
        )

property_sector = CRUDPropertySector(PropertySector)
sector_inn = CRUDSectorInn(SectorInn)
