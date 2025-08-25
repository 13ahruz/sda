from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from ..core.db import get_db
from ..crud.work_process import work_process
from ..schemas.work_process import (
    WorkProcessCreate,
    WorkProcessRead,
    WorkProcessUpdate
)
from ..utils.uploads import upload_file

router = APIRouter()

@router.get("/work-processes", response_model=List[WorkProcessRead])
@cache(expire=300)
async def list_work_processes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all work processes"""
    return work_process.get_multi_ordered(db, skip=skip, limit=limit)

@router.post("/work-processes", response_model=WorkProcessRead)
async def create_work_process(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    order: int = Form(0),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Create a new work process with form data and optional image"""
    image_url = None
    if image:
        image_url = await upload_file(image, "work-processes", request)
    
    process_data = WorkProcessCreate(
        title=title,
        description=description,
        order=order,
        image_url=image_url
    )
    return work_process.create(db=db, obj_in=process_data)

@router.post("/work-processes/json", response_model=WorkProcessRead)
async def create_work_process_json(
    process_in: WorkProcessCreate,
    db: Session = Depends(get_db)
):
    """Create a new work process with JSON data (for backwards compatibility)"""
    return work_process.create(db=db, obj_in=process_in)

@router.post("/work-processes/{process_id}/photo")
async def upload_work_process_photo(
    process_id: int,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload photo for a work process"""
    db_process = work_process.get(db, id=process_id)
    if not db_process:
        raise HTTPException(status_code=404, detail="Work process not found")
    
    file_url = await upload_file(file, "work-processes", request)
    work_process.update(db=db, db_obj=db_process, obj_in={"photo_url": file_url})
    return {"message": "Photo uploaded successfully", "url": file_url}

@router.get("/work-processes/{process_id}", response_model=WorkProcessRead)
@cache(expire=300)
async def get_work_process(
    process_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific work process by ID"""
    db_process = work_process.get(db, id=process_id)
    if not db_process:
        raise HTTPException(status_code=404, detail="Work process not found")
    return db_process

@router.put("/work-processes/{process_id}", response_model=WorkProcessRead)
async def update_work_process(
    process_id: int,
    process_in: WorkProcessUpdate,
    db: Session = Depends(get_db)
):
    """Update a work process"""
    db_process = work_process.get(db, id=process_id)
    if not db_process:
        raise HTTPException(status_code=404, detail="Work process not found")
    return work_process.update(db=db, db_obj=db_process, obj_in=process_in)

@router.delete("/work-processes/{process_id}")
async def delete_work_process(
    process_id: int,
    db: Session = Depends(get_db)
):
    """Delete a work process"""
    db_process = work_process.get(db, id=process_id)
    if not db_process:
        raise HTTPException(status_code=404, detail="Work process not found")
    work_process.remove(db=db, id=process_id)
    return {"message": "Work process deleted successfully"}
