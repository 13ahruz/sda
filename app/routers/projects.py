from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from ..core.db import get_db
from ..crud.projects import project, project_photo
from ..schemas.projects import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
    ProjectPhotoCreate,
    ProjectPhotoRead,
    ProjectPhotoUpdate
)
from ..utils.uploads import upload_file

router = APIRouter()

# Project endpoints
@router.get("/projects", response_model=List[ProjectRead])
@cache(expire=300)
async def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    property_sector_id: Optional[int] = Query(None),
    year: Optional[int] = Query(None),
    tag: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all projects with optional filters"""
    return project.get_multi_filtered(
        db, 
        skip=skip, 
        limit=limit,
        property_sector_id=property_sector_id,
        year=year,
        tag=tag
    )

@router.post("/projects", response_model=ProjectRead)
async def create_project(
    title: str = Form(...),
    tag: str = Form(...),
    client: str = Form(...),
    year: int = Form(...),
    property_sector_id: int = Form(...),
    cover_photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Create a new project with form data and optional cover photo"""
    cover_photo_url = None
    if cover_photo:
        cover_photo_url = await upload_file(cover_photo, "projects/covers")
    
    project_data = ProjectCreate(
        title=title,
        tag=tag,
        client=client,
        year=year,
        property_sector_id=property_sector_id,
        cover_photo_url=cover_photo_url,
        photos=[]
    )
    return project.create(db=db, obj_in=project_data)

@router.post("/projects/json", response_model=ProjectRead)
async def create_project_json(
    project_in: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project with JSON data (for backwards compatibility)"""
    return project.create(db=db, obj_in=project_in)

@router.post("/projects/{project_id}/cover-photo")
async def upload_project_cover_photo(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload cover photo for a project"""
    db_project = project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    file_url = await upload_file(file, "projects/covers")
    project.update(db=db, db_obj=db_project, obj_in={"cover_photo_url": file_url})
    return {"message": "Cover photo uploaded successfully", "url": file_url}

@router.get("/projects/{project_id}", response_model=ProjectRead)
@cache(expire=300)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific project by ID"""
    db_project = project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/projects/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Update a project"""
    db_project = project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.update(db=db, db_obj=db_project, obj_in=project_in)

@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Delete a project"""
    db_project = project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.remove(db=db, id=project_id)
    return {"message": "Project deleted successfully"}

# Project Photo endpoints
@router.get("/projects/{project_id}/photos", response_model=List[ProjectPhotoRead])
@cache(expire=300)
async def list_project_photos(
    project_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all photos for a project"""
    return project_photo.get_by_project(db, project_id=project_id, skip=skip, limit=limit)

@router.post("/projects/{project_id}/photos")
async def upload_project_photo(
    project_id: int,
    file: UploadFile = File(...),
    order: int = Query(0),
    db: Session = Depends(get_db)
):
    """Upload a photo for a project"""
    db_project = project.get(db, id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    file_url = await upload_file(file, "projects/photos")
    photo_data = ProjectPhotoCreate(project_id=project_id, order=order)
    db_photo = project_photo.create(db=db, obj_in=photo_data)
    project_photo.update(db=db, db_obj=db_photo, obj_in={"image_url": file_url})
    return {"message": "Photo uploaded successfully", "url": file_url, "id": db_photo.id}

@router.get("/project-photos/{photo_id}", response_model=ProjectPhotoRead)
@cache(expire=300)
async def get_project_photo(
    photo_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific project photo by ID"""
    db_photo = project_photo.get(db, id=photo_id)
    if not db_photo:
        raise HTTPException(status_code=404, detail="Project photo not found")
    return db_photo

@router.put("/project-photos/{photo_id}", response_model=ProjectPhotoRead)
async def update_project_photo(
    photo_id: int,
    photo_in: ProjectPhotoUpdate,
    db: Session = Depends(get_db)
):
    """Update a project photo"""
    db_photo = project_photo.get(db, id=photo_id)
    if not db_photo:
        raise HTTPException(status_code=404, detail="Project photo not found")
    return project_photo.update(db=db, db_obj=db_photo, obj_in=photo_in)

@router.delete("/project-photos/{photo_id}")
async def delete_project_photo(
    photo_id: int,
    db: Session = Depends(get_db)
):
    """Delete a project photo"""
    db_photo = project_photo.get(db, id=photo_id)
    if not db_photo:
        raise HTTPException(status_code=404, detail="Project photo not found")
    project_photo.remove(db=db, id=photo_id)
    return {"message": "Project photo deleted successfully"}
