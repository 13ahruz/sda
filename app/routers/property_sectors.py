from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Form
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from ..core.db import get_db
from ..crud.property_sectors import property_sector, sector_inn
from ..schemas.property_sectors import (
    PropertySectorCreate,
    PropertySectorRead,
    PropertySectorUpdate,
    SectorInnCreate,
    SectorInnRead,
    SectorInnUpdate
)

router = APIRouter()

# PropertySector endpoints
@router.get("/property-sectors", response_model=List[PropertySectorRead])
@cache(expire=300)
async def list_property_sectors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all property sectors ordered by order field"""
    return property_sector.get_multi_ordered(db, skip=skip, limit=limit)

@router.post("/property-sectors", response_model=PropertySectorRead)
async def create_property_sector(
    title: str = Form(...),
    description: str = Form(...),
    order: int = Form(0),
    db: Session = Depends(get_db)
):
    """Create a new property sector with form data"""
    property_sector_data = PropertySectorCreate(
        title=title,
        description=description,
        order=order
    )
    return property_sector.create(db=db, obj_in=property_sector_data)

@router.post("/property-sectors/json", response_model=PropertySectorRead)
async def create_property_sector_json(
    property_sector_in: PropertySectorCreate,
    db: Session = Depends(get_db)
):
    """Create a new property sector with JSON data (for backwards compatibility)"""
    return property_sector.create(db=db, obj_in=property_sector_in)

@router.get("/property-sectors/{property_sector_id}", response_model=PropertySectorRead)
@cache(expire=300)
async def get_property_sector(
    property_sector_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific property sector by ID"""
    db_property_sector = property_sector.get(db, id=property_sector_id)
    if not db_property_sector:
        raise HTTPException(status_code=404, detail="Property sector not found")
    return db_property_sector

@router.put("/property-sectors/{property_sector_id}", response_model=PropertySectorRead)
async def update_property_sector(
    property_sector_id: int,
    property_sector_in: PropertySectorUpdate,
    db: Session = Depends(get_db)
):
    """Update a property sector"""
    db_property_sector = property_sector.get(db, id=property_sector_id)
    if not db_property_sector:
        raise HTTPException(status_code=404, detail="Property sector not found")
    return property_sector.update(db=db, db_obj=db_property_sector, obj_in=property_sector_in)

@router.delete("/property-sectors/{property_sector_id}")
async def delete_property_sector(
    property_sector_id: int,
    db: Session = Depends(get_db)
):
    """Delete a property sector"""
    db_property_sector = property_sector.get(db, id=property_sector_id)
    if not db_property_sector:
        raise HTTPException(status_code=404, detail="Property sector not found")
    property_sector.remove(db=db, id=property_sector_id)
    return {"message": "Property sector deleted successfully"}

# SectorInn endpoints
@router.get("/property-sectors/{property_sector_id}/inns", response_model=List[SectorInnRead])
@cache(expire=300)
async def list_sector_inns(
    property_sector_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all sector inns for a property sector"""
    return sector_inn.get_by_property_sector(db, property_sector_id=property_sector_id, skip=skip, limit=limit)

@router.post("/sector-inns", response_model=SectorInnRead)
async def create_sector_inn(
    title: str = Form(...),
    description: str = Form(...),
    property_sector_id: int = Form(...),
    order: int = Form(0),
    db: Session = Depends(get_db)
):
    """Create a new sector inn with form data"""
    sector_inn_data = SectorInnCreate(
        title=title,
        description=description,
        property_sector_id=property_sector_id,
        order=order
    )
    return sector_inn.create(db=db, obj_in=sector_inn_data)

@router.post("/sector-inns/json", response_model=SectorInnRead)
async def create_sector_inn_json(
    sector_inn_in: SectorInnCreate,
    db: Session = Depends(get_db)
):
    """Create a new sector inn with JSON data (for backwards compatibility)"""
    return sector_inn.create(db=db, obj_in=sector_inn_in)

@router.get("/sector-inns/{sector_inn_id}", response_model=SectorInnRead)
@cache(expire=300)
async def get_sector_inn(
    sector_inn_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific sector inn by ID"""
    db_sector_inn = sector_inn.get(db, id=sector_inn_id)
    if not db_sector_inn:
        raise HTTPException(status_code=404, detail="Sector inn not found")
    return db_sector_inn

@router.put("/sector-inns/{sector_inn_id}", response_model=SectorInnRead)
async def update_sector_inn(
    sector_inn_id: int,
    sector_inn_in: SectorInnUpdate,
    db: Session = Depends(get_db)
):
    """Update a sector inn"""
    db_sector_inn = sector_inn.get(db, id=sector_inn_id)
    if not db_sector_inn:
        raise HTTPException(status_code=404, detail="Sector inn not found")
    return sector_inn.update(db=db, db_obj=db_sector_inn, obj_in=sector_inn_in)

@router.delete("/sector-inns/{sector_inn_id}")
async def delete_sector_inn(
    sector_inn_id: int,
    db: Session = Depends(get_db)
):
    """Delete a sector inn"""
    db_sector_inn = sector_inn.get(db, id=sector_inn_id)
    if not db_sector_inn:
        raise HTTPException(status_code=404, detail="Sector inn not found")
    sector_inn.remove(db=db, id=sector_inn_id)
    return {"message": "Sector inn deleted successfully"}
