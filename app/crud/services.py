from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.services import Service, ServiceBenefit
from ..schemas.services import ServiceCreate, ServiceUpdate, ServiceBenefitCreate, ServiceBenefitUpdate
from .base import CRUDBase

class CRUDService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[Service]:
        return db.query(Service).filter(Service.slug == slug).first()

class CRUDServiceBenefit(CRUDBase[ServiceBenefit, ServiceBenefitCreate, ServiceBenefitUpdate]):
    pass

service = CRUDService(Service)
service_benefit = CRUDServiceBenefit(ServiceBenefit)
