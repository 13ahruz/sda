from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Form
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from ..core.db import get_db
from ..crud.approaches import approach
from ..schemas.approaches import (
    ApproachCreate,
    ApproachRead,
    ApproachUpdate
)

router = APIRouter()

@router.get("/approaches", response_model=List[ApproachRead])
@cache(expire=300)  # Cache for 5 minutes
async def list_approaches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all approaches ordered by order field"""
    return approach.get_multi_ordered(db, skip=skip, limit=limit)

@router.post("/approaches", response_model=ApproachRead)
async def create_approach(
    title: str = Form(...),
    description: str = Form(None),
    order: int = Form(0),
    db: Session = Depends(get_db)
):
    """Create a new approach with form data"""
    approach_data = ApproachCreate(
        title=title,
        description=description,
        order=order
    )
    return approach.create(db=db, obj_in=approach_data)

@router.post("/approaches/json", response_model=ApproachRead)
async def create_approach_json(
    approach_in: ApproachCreate,
    db: Session = Depends(get_db)
):
    """Create a new approach with JSON data (for backwards compatibility)"""
    return approach.create(db=db, obj_in=approach_in)

@router.get("/approaches/{approach_id}", response_model=ApproachRead)
@cache(expire=300)
async def get_approach(
    approach_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific approach by ID"""
    db_approach = approach.get(db, id=approach_id)
    if not db_approach:
        raise HTTPException(status_code=404, detail="Approach not found")
    return db_approach

@router.put("/approaches/{approach_id}", response_model=ApproachRead)
async def update_approach(
    approach_id: int,
    approach_in: ApproachUpdate,
    db: Session = Depends(get_db)
):
    """Update an approach"""
    db_approach = approach.get(db, id=approach_id)
    if not db_approach:
        raise HTTPException(status_code=404, detail="Approach not found")
    return approach.update(db=db, db_obj=db_approach, obj_in=approach_in)

@router.delete("/approaches/{approach_id}")
async def delete_approach(
    approach_id: int,
    db: Session = Depends(get_db)
):
    """Delete an approach"""
    db_approach = approach.get(db, id=approach_id)
    if not db_approach:
        raise HTTPException(status_code=404, detail="Approach not found")
    approach.remove(db=db, id=approach_id)
    return {"message": "Approach deleted successfully"}
