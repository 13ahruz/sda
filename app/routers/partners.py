from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from ..core.db import get_db
from ..crud.partners import partner, partner_logo
from ..schemas.partners import (
    PartnerCreate,
    PartnerRead,
    PartnerUpdate,
    PartnerLogoCreate,
    PartnerLogoRead,
    PartnerLogoUpdate
)
from ..utils.uploads import upload_file
from ..utils.multilingual import prepare_multilingual_response, validate_language

router = APIRouter()

# Partner endpoints
@router.get("/partners")
@cache(expire=300)
async def list_partners(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    language: str = Query("en", description="Language code (en, az, ru)"),
    db: Session = Depends(get_db)
):
    """Get all partners with multilingual support"""
    lang = validate_language(language)
    partners = partner.get_multi(db, skip=skip, limit=limit)
    
    # Prepare multilingual response
    multilingual_partners = []
    for ptnr in partners:
        multilingual_ptnr = prepare_multilingual_response(
            ptnr, 
            ['title', 'button_text'], 
            lang
        )
        multilingual_partners.append(multilingual_ptnr)
    
    return multilingual_partners

@router.post("/partners", response_model=PartnerRead)
async def create_partner(
    title: str = Form(...),
    button_text: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create a new partner with form data"""
    partner_data = PartnerCreate(
        title=title,
        button_text=button_text
    )
    return partner.create(db=db, obj_in=partner_data)

@router.post("/partners/json", response_model=PartnerRead)
async def create_partner_json(
    partner_in: PartnerCreate,
    db: Session = Depends(get_db)
):
    """Create a new partner with JSON data (for backwards compatibility)"""
    return partner.create(db=db, obj_in=partner_in)

@router.get("/partners/{partner_id}", response_model=PartnerRead)
@cache(expire=300)
async def get_partner(
    partner_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific partner by ID"""
    db_partner = partner.get(db, id=partner_id)
    if not db_partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return db_partner

@router.put("/partners/{partner_id}", response_model=PartnerRead)
async def update_partner(
    partner_id: int,
    partner_in: PartnerUpdate,
    db: Session = Depends(get_db)
):
    """Update a partner"""
    db_partner = partner.get(db, id=partner_id)
    if not db_partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    return partner.update(db=db, db_obj=db_partner, obj_in=partner_in)

@router.delete("/partners/{partner_id}")
async def delete_partner(
    partner_id: int,
    db: Session = Depends(get_db)
):
    """Delete a partner"""
    db_partner = partner.get(db, id=partner_id)
    if not db_partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    partner.remove(db=db, id=partner_id)
    return {"message": "Partner deleted successfully"}

# Partner Logo endpoints
@router.get("/partners/{partner_id}/logos", response_model=List[PartnerLogoRead])
@cache(expire=300)
async def list_partner_logos(
    partner_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all logos for a partner"""
    return partner_logo.get_by_partner(db, partner_id=partner_id, skip=skip, limit=limit)

@router.post("/partners/{partner_id}/logos")
async def upload_partner_logo(
    partner_id: int,
    request: Request,
    file: UploadFile = File(...),
    order: int = Query(0),
    db: Session = Depends(get_db)
):
    """Upload a logo for a partner"""
    db_partner = partner.get(db, id=partner_id)
    if not db_partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    file_url = await upload_file(file, "partners/logos", request)
    logo_data = PartnerLogoCreate(partner_id=partner_id, order=order)
    db_logo = partner_logo.create(db=db, obj_in=logo_data)
    partner_logo.update(db=db, db_obj=db_logo, obj_in={"image_url": file_url})
    return {"message": "Logo uploaded successfully", "url": file_url, "id": db_logo.id}
