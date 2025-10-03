from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from ..core.db import get_db
from ..crud.team import team_member, team_section, team_section_item
from ..schemas.team import (
    TeamMemberCreate,
    TeamMemberRead,
    TeamMemberUpdate,
    TeamSectionCreate,
    TeamSectionRead,
    TeamSectionUpdate,
    TeamSectionItemCreate,
    TeamSectionItemRead,
    TeamSectionItemUpdate
)
from ..utils.uploads import upload_file
from ..utils.multilingual import prepare_multilingual_response, validate_language

router = APIRouter()

# TeamMember endpoints (full roster)
@router.get("/team-members")
@cache(expire=300)
async def list_team_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    language: str = Query("en", description="Language code (en, az, ru)"),
    db: Session = Depends(get_db)
):
    """Get all team members for full roster with multilingual support"""
    lang = validate_language(language)
    members = team_member.get_multi_ordered(db, skip=skip, limit=limit)
    
    # Prepare multilingual response
    multilingual_members = []
    for member in members:
        multilingual_member = prepare_multilingual_response(
            member, 
            ['full_name', 'role'], 
            lang
        )
        multilingual_members.append(multilingual_member)
    
    return multilingual_members

@router.post("/team-members", response_model=TeamMemberRead)
async def create_team_member(
    request: Request,
    full_name: str = Form(...),
    role: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Create a new team member with form data and optional photo"""
    photo_url = None
    if photo:
        photo_url = await upload_file(photo, "team/members", request)
    
    member_data = TeamMemberCreate(
        full_name=full_name,
        role=role,
        photo_url=photo_url
    )
    return team_member.create(db=db, obj_in=member_data)

@router.post("/team-members/json", response_model=TeamMemberRead)
async def create_team_member_json(
    member_in: TeamMemberCreate,
    db: Session = Depends(get_db)
):
    """Create a new team member with JSON data (for backwards compatibility)"""
    return team_member.create(db=db, obj_in=member_in)

@router.post("/team-members/{member_id}/photo")
async def upload_team_member_photo(
    member_id: int,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload photo for a team member"""
    db_member = team_member.get(db, id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    file_url = await upload_file(file, "team/members", request)
    team_member.update(db=db, db_obj=db_member, obj_in={"photo_url": file_url})
    return {"message": "Photo uploaded successfully", "url": file_url}

@router.get("/team-members/{member_id}")
@cache(expire=300)
async def get_team_member(
    member_id: int,
    language: str = Query("en", description="Language code (en, az, ru)"),
    db: Session = Depends(get_db)
):
    """Get a specific team member by ID with multilingual support"""
    db_member = team_member.get(db, id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    lang = validate_language(language)
    return prepare_multilingual_response(
        db_member, 
        ['full_name', 'role'], 
        lang
    )

@router.put("/team-members/{member_id}", response_model=TeamMemberRead)
async def update_team_member(
    member_id: int,
    member_in: TeamMemberUpdate,
    db: Session = Depends(get_db)
):
    """Update a team member"""
    db_member = team_member.get(db, id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    return team_member.update(db=db, db_obj=db_member, obj_in=member_in)

@router.delete("/team-members/{member_id}")
async def delete_team_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    """Delete a team member"""
    db_member = team_member.get(db, id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    team_member.remove(db=db, id=member_id)
    return {"message": "Team member deleted successfully"}

# TeamSection endpoints (section with list)
@router.get("/team-sections", response_model=List[TeamSectionRead])
@cache(expire=300)
async def list_team_sections(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all team sections"""
    return team_section.get_multi(db, skip=skip, limit=limit)

@router.post("/team-sections", response_model=TeamSectionRead)
async def create_team_section(
    title: str = Form(...),
    button_text: str = Form(None),
    db: Session = Depends(get_db)
):
    """Create a new team section with form data"""
    section_data = TeamSectionCreate(
        title=title,
        button_text=button_text
    )
    return team_section.create(db=db, obj_in=section_data)

@router.post("/team-sections/json", response_model=TeamSectionRead)
async def create_team_section_json(
    section_in: TeamSectionCreate,
    db: Session = Depends(get_db)
):
    """Create a new team section with JSON data (for backwards compatibility)"""
    return team_section.create(db=db, obj_in=section_in)

@router.get("/team-sections/{section_id}", response_model=TeamSectionRead)
@cache(expire=300)
async def get_team_section(
    section_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific team section by ID"""
    db_section = team_section.get(db, id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Team section not found")
    return db_section

@router.put("/team-sections/{section_id}", response_model=TeamSectionRead)
async def update_team_section(
    section_id: int,
    section_in: TeamSectionUpdate,
    db: Session = Depends(get_db)
):
    """Update a team section"""
    db_section = team_section.get(db, id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Team section not found")
    return team_section.update(db=db, db_obj=db_section, obj_in=section_in)

@router.delete("/team-sections/{section_id}")
async def delete_team_section(
    section_id: int,
    db: Session = Depends(get_db)
):
    """Delete a team section"""
    db_section = team_section.get(db, id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="Team section not found")
    team_section.remove(db=db, id=section_id)
    return {"message": "Team section deleted successfully"}

# TeamSectionItem endpoints
@router.get("/team-sections/{section_id}/items", response_model=List[TeamSectionItemRead])
@cache(expire=300)
async def list_team_section_items(
    section_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all items for a team section"""
    return team_section_item.get_by_section(db, section_id=section_id, skip=skip, limit=limit)

@router.post("/team-sections/{section_id}/items", response_model=TeamSectionItemRead)
async def create_team_section_item(
    section_id: int,
    item_in: TeamSectionItemCreate,
    db: Session = Depends(get_db)
):
    """Create a new team section item"""
    item_in.team_section_id = section_id
    return team_section_item.create(db=db, obj_in=item_in)

@router.post("/team-section-items/{item_id}/photo")
async def upload_team_section_item_photo(
    item_id: int,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload photo for a team section item"""
    db_item = team_section_item.get(db, id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Team section item not found")
    
    file_url = await upload_file(file, "team/sections", request)
    team_section_item.update(db=db, db_obj=db_item, obj_in={"photo_url": file_url})
    return {"message": "Photo uploaded successfully", "url": file_url}

@router.get("/team-section-items/{item_id}", response_model=TeamSectionItemRead)
@cache(expire=300)
async def get_team_section_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific team section item by ID"""
    db_item = team_section_item.get(db, id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Team section item not found")
    return db_item

@router.put("/team-section-items/{item_id}", response_model=TeamSectionItemRead)
async def update_team_section_item(
    item_id: int,
    item_in: TeamSectionItemUpdate,
    db: Session = Depends(get_db)
):
    """Update a team section item"""
    db_item = team_section_item.get(db, id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Team section item not found")
    return team_section_item.update(db=db, db_obj=db_item, obj_in=item_in)

@router.delete("/team-section-items/{item_id}")
async def delete_team_section_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete a team section item"""
    db_item = team_section_item.get(db, id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Team section item not found")
    team_section_item.remove(db=db, id=item_id)
    return {"message": "Team section item deleted successfully"}
