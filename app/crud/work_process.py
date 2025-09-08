from typing import List
from sqlalchemy.orm import Session
from ..crud.base import CRUDBase
from ..models.work_process import WorkProcess
from ..schemas.work_process import WorkProcessCreate, WorkProcessUpdate

class CRUDWorkProcess(CRUDBase[WorkProcess, WorkProcessCreate, WorkProcessUpdate]):
    def get_multi_ordered(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[WorkProcess]:
        """Get work processes ordered by order field"""
        return (
            db.query(self.model)
            .order_by(self.model.order.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

work_process = CRUDWorkProcess(WorkProcess)
