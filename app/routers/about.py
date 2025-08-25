from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from ..core.db import get_db
from ..crud.about import about, about_logo
from ..schemas.about import (
    AboutCreate,
    AboutRead,
    AboutUpdate,
    AboutLogoCreate,
    AboutLogoRead,
    AboutLogoUpdate
)
from ..utils.uploads import upload_file

router = APIRouter()

# About endpoints
@router.get("/about", response_model=List[AboutRead])
@cache(expire=300)
async def list_about_sections(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all about sections"""
    return about.get_multi_ordered(db, skip=skip, limit=limit)

@router.post("/about", response_model=AboutRead)
async def create_about_section(
    experience: str = Form(...),
    project_count: str = Form(...),
    members: str = Form(...),
    db: Session = Depends(get_db)
):
    """Create a new about section with form data"""
    about_data = AboutCreate(
        experience=experience,
        project_count=project_count,
        members=members
    )
    return about.create(db=db, obj_in=about_data)

@router.post("/about/json", response_model=AboutRead)
async def create_about_section_json(
    about_in: AboutCreate,
    db: Session = Depends(get_db)
):
    """Create a new about section with JSON data (for backwards compatibility)"""
    return about.create(db=db, obj_in=about_in)

@router.post("/about/{about_id}/photo")
async def upload_about_photo(
    about_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload photo for an about section"""
    db_about = about.get(db, id=about_id)
    if not db_about:
        raise HTTPException(status_code=404, detail="About section not found")
    
    file_url = await upload_file(file, "about/photos")
    about.update(db=db, db_obj=db_about, obj_in={"photo_url": file_url})
    return {"message": "Photo uploaded successfully", "url": file_url}

@router.get("/about/{about_id}", response_model=AboutRead)
@cache(expire=300)
async def get_about_section(
    about_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific about section by ID"""
    db_about = about.get(db, id=about_id)
    if not db_about:
        raise HTTPException(status_code=404, detail="About section not found")
    return db_about

@router.put("/about/{about_id}", response_model=AboutRead)
async def update_about_section(
    about_id: int,
    about_in: AboutUpdate,
    db: Session = Depends(get_db)
):
    """Update an about section"""
    db_about = about.get(db, id=about_id)
    if not db_about:
        raise HTTPException(status_code=404, detail="About section not found")
    return about.update(db=db, db_obj=db_about, obj_in=about_in)

@router.delete("/about/{about_id}")
async def delete_about_section(
    about_id: int,
    db: Session = Depends(get_db)
):
    """Delete an about section"""
    db_about = about.get(db, id=about_id)
    if not db_about:
        raise HTTPException(status_code=404, detail="About section not found")
    about.remove(db=db, id=about_id)
    return {"message": "About section deleted successfully"}

# AboutLogo endpoints
@router.get("/about/{about_id}/logos", response_model=List[AboutLogoRead])
@cache(expire=300)
async def list_about_logos(
    about_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all logos for an about section"""
    return about_logo.get_by_about(db, about_id=about_id, skip=skip, limit=limit)

@router.post("/about/{about_id}/logos", response_model=AboutLogoRead)
async def create_about_logo(
    about_id: int,
    logo_in: AboutLogoCreate,
    db: Session = Depends(get_db)
):
    """Create a new logo for an about section"""
    logo_in.about_id = about_id
    return about_logo.create(db=db, obj_in=logo_in)

@router.post("/about-logos/{logo_id}/upload")
async def upload_about_logo_file(
    logo_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload logo file for an about logo"""
    db_logo = about_logo.get(db, id=logo_id)
    if not db_logo:
        raise HTTPException(status_code=404, detail="About logo not found")
    
    file_url = await upload_file(file, "about/logos")
    about_logo.update(db=db, db_obj=db_logo, obj_in={"logo_url": file_url})
    return {"message": "Logo uploaded successfully", "url": file_url}

@router.get("/about-logos/{logo_id}", response_model=AboutLogoRead)
@cache(expire=300)
async def get_about_logo(
    logo_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific about logo by ID"""
    db_logo = about_logo.get(db, id=logo_id)
    if not db_logo:
        raise HTTPException(status_code=404, detail="About logo not found")
    return db_logo

@router.put("/about-logos/{logo_id}", response_model=AboutLogoRead)
async def update_about_logo(
    logo_id: int,
    logo_in: AboutLogoUpdate,
    db: Session = Depends(get_db)
):
    """Update an about logo"""
    db_logo = about_logo.get(db, id=logo_id)
    if not db_logo:
        raise HTTPException(status_code=404, detail="About logo not found")
    return about_logo.update(db=db, db_obj=db_logo, obj_in=logo_in)

@router.delete("/about-logos/{logo_id}")
async def delete_about_logo(
    logo_id: int,
    db: Session = Depends(get_db)
):
    """Delete an about logo"""
    db_logo = about_logo.get(db, id=logo_id)
    if not db_logo:
        raise HTTPException(status_code=404, detail="About logo not found")
    about_logo.remove(db=db, id=logo_id)
    return {"message": "About logo deleted successfully"}
