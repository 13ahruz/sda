from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.services import Service, ServiceBenefit
from ..schemas.services import ServiceCreate, ServiceUpdate, ServiceBenefitCreate, ServiceBenefitUpdate
from .base import CRUDBase

class CRUDService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    pass

class CRUDServiceBenefit(CRUDBase[ServiceBenefit, ServiceBenefitCreate, ServiceBenefitUpdate]):
    pass

service = CRUDService(Service)
service_benefit = CRUDServiceBenefit(ServiceBenefit)
