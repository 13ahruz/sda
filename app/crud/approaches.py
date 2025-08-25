from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc
from ..crud.base import CRUDBase
from ..models.approaches import Approach
from ..schemas.approaches import ApproachCreate, ApproachUpdate

class CRUDApproach(CRUDBase[Approach, ApproachCreate, ApproachUpdate]):
    def get_multi_ordered(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Approach]:
        return (
            db.query(self.model)
            .order_by(asc(self.model.order), asc(self.model.id))
            .offset(skip)
            .limit(limit)
            .all()
        )

approach = CRUDApproach(Approach)
