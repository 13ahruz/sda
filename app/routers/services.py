from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from ..core.db import get_db
from ..crud.services import service, service_benefit
from ..schemas.services import (
    ServiceCreate,
    ServiceRead,
    ServiceUpdate,
    ServiceBenefitCreate,
    ServiceBenefitRead,
    ServiceBenefitUpdate
)
from ..utils.uploads import upload_file

router = APIRouter()

@router.get("/services", response_model=List[ServiceRead])
@cache(expire=300)  # Cache for 5 minutes
async def list_services(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    order_by: Optional[str] = None,
    direction: str = Query("asc", regex="^(asc|desc)$")
):
    return service.get_multi(
        db,
        skip=skip,
        limit=limit,
        order_by=order_by,
        direction=direction
    )

router = APIRouter()

@router.get("/services", response_model=List[ServiceRead])
@cache(expire=300)  # Cache for 5 minutes
async def list_services(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    order_by: Optional[str] = None,
    direction: str = Query("asc", regex="^(asc|desc)$")
):
    return service.get_multi(
        db,
        skip=skip,
        limit=limit,
        order_by=order_by,
        direction=direction
    )

@router.post("/services", response_model=ServiceRead)
async def create_service(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    order: int = Form(0),
    icon: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Create a new service with form data and optional icon upload"""
    icon_url = None
    if icon:
        icon_url = await upload_file(icon, "services/icons", request)
    
    service_data = ServiceCreate(
        name=name,
        description=description,
        order=order,
        icon_url=icon_url
    )
    return service.create(db=db, obj_in=service_data)

@router.post("/services/json", response_model=ServiceRead)
def create_service_json(
    *,
    db: Session = Depends(get_db),
    service_in: ServiceCreate
):
    """Create a service with JSON data (for backwards compatibility)"""
    return service.create(db=db, obj_in=service_in)

@router.get("/services/{service_id}", response_model=ServiceRead)
def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    db_service = service.get(db=db, id=service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service

@router.get("/services/slug/{service_slug}", response_model=ServiceRead)
def get_service_by_slug(
    service_slug: str,
    db: Session = Depends(get_db)
):
    db_service = service.get_by_slug(db=db, slug=service_slug)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service

@router.patch("/services/{service_id}", response_model=ServiceRead)
def update_service(
    *,
    db: Session = Depends(get_db),
    service_id: int,
    service_in: ServiceUpdate
):
    db_service = service.get(db=db, id=service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service.update(db=db, db_obj=db_service, obj_in=service_in)

@router.delete("/services/{service_id}", response_model=ServiceRead)
def delete_service(
    *,
    db: Session = Depends(get_db),
    service_id: int
):
    return service.remove(db=db, id=service_id)

# Service Benefits endpoints

@router.get("/service-benefits", response_model=List[ServiceBenefitRead])
@cache(expire=300)  # Cache for 5 minutes
async def list_service_benefits(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    order_by: Optional[str] = None,
    direction: str = Query("asc", regex="^(asc|desc)$")
):
    return service_benefit.get_multi(
        db,
        skip=skip,
        limit=limit,
        order_by=order_by,
        direction=direction
    )

@router.post("/service-benefits", response_model=ServiceBenefitRead)
def create_service_benefit(
    *,
    db: Session = Depends(get_db),
    benefit_in: ServiceBenefitCreate
):
    return service_benefit.create(db=db, obj_in=benefit_in)

@router.get("/service-benefits/{benefit_id}", response_model=ServiceBenefitRead)
def get_service_benefit(
    benefit_id: int,
    db: Session = Depends(get_db)
):
    db_benefit = service_benefit.get(db=db, id=benefit_id)
    if not db_benefit:
        raise HTTPException(status_code=404, detail="Service benefit not found")
    return db_benefit

@router.patch("/service-benefits/{benefit_id}", response_model=ServiceBenefitRead)
def update_service_benefit(
    *,
    db: Session = Depends(get_db),
    benefit_id: int,
    benefit_in: ServiceBenefitUpdate
):
    db_benefit = service_benefit.get(db=db, id=benefit_id)
    if not db_benefit:
        raise HTTPException(status_code=404, detail="Service benefit not found")
    return service_benefit.update(db=db, db_obj=db_benefit, obj_in=benefit_in)

@router.delete("/service-benefits/{benefit_id}", response_model=ServiceBenefitRead)
def delete_service_benefit(
    *,
    db: Session = Depends(get_db),
    benefit_id: int
):
    return service_benefit.remove(db=db, id=benefit_id)
