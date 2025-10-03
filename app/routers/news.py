from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from ..core.db import get_db
from ..crud.news import news, news_section
from ..schemas.news import (
    NewsCreate,
    NewsRead,
    NewsUpdate,
    NewsSectionCreate,
    NewsSectionRead,
    NewsSectionUpdate
)
from ..utils.uploads import upload_file
from ..utils.multilingual import prepare_multilingual_response, validate_language

router = APIRouter()

# News endpoints
@router.get("/news")
@cache(expire=300)
async def list_news(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tags: Optional[List[str]] = Query(None),
    language: str = Query("en", description="Language code (en, az, ru)"),
    db: Session = Depends(get_db)
):
    """Get all news with optional tag filtering and multilingual support"""
    lang = validate_language(language)
    news_items = news.get_multi_filtered(db, skip=skip, limit=limit, tags=tags)
    
    # Prepare multilingual response
    multilingual_news = []
    for news_item in news_items:
        multilingual_news_item = prepare_multilingual_response(
            news_item, 
            ['title', 'description', 'content'], 
            lang
        )
        multilingual_news.append(multilingual_news_item)
    
    return multilingual_news

@router.post("/news", response_model=NewsRead)
async def create_news(
    request: Request,
    title: str = Form(...),
    summary: str = Form(...),
    tags: str = Form(""),  # Comma-separated tags
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """Create a new news article with form data and optional photo"""
    photo_url = None
    if photo:
        photo_url = await upload_file(photo, "news", request)
    
    # Convert comma-separated tags to list
    tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()] if tags else []
    
    news_data = NewsCreate(
        title=title,
        summary=summary,
        tags=tags_list,
        photo_url=photo_url
    )
    return news.create(db=db, obj_in=news_data)

@router.post("/news/json", response_model=NewsRead)
async def create_news_json(
    news_in: NewsCreate,
    db: Session = Depends(get_db)
):
    """Create a new news article with JSON data (for backwards compatibility)"""
    return news.create(db=db, obj_in=news_in)

@router.post("/news/{news_id}/photo")
async def upload_news_photo(
    news_id: int,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload photo for a news article"""
    db_news = news.get(db, id=news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    
    file_url = await upload_file(file, "news", request)
    news.update(db=db, db_obj=db_news, obj_in={"photo_url": file_url})
    return {"message": "Photo uploaded successfully", "url": file_url}

@router.get("/news/{news_id}")
@cache(expire=300)
async def get_news(
    news_id: int,
    language: str = Query("en", description="Language code (en, az, ru)"),
    db: Session = Depends(get_db)
):
    """Get a specific news article by ID with multilingual support"""
    db_news = news.get(db, id=news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    
    lang = validate_language(language)
    return prepare_multilingual_response(
        db_news, 
        ['title', 'description', 'content'], 
        lang
    )

@router.get("/news/slug/{news_slug}")
@cache(expire=300)
async def get_news_by_slug(
    news_slug: str,
    language: str = Query("en", description="Language code (en, az, ru)"),
    db: Session = Depends(get_db)
):
    """Get a specific news article by slug with multilingual support"""
    db_news = news.get_by_slug(db, slug=news_slug)
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    
    lang = validate_language(language)
    return prepare_multilingual_response(
        db_news, 
        ['title', 'description', 'content'], 
        lang
    )

@router.put("/news/{news_id}", response_model=NewsRead)
async def update_news(
    news_id: int,
    news_in: NewsUpdate,
    db: Session = Depends(get_db)
):
    """Update a news article"""
    db_news = news.get(db, id=news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    return news.update(db=db, db_obj=db_news, obj_in=news_in)

@router.delete("/news/{news_id}")
async def delete_news(
    news_id: int,
    db: Session = Depends(get_db)
):
    """Delete a news article"""
    db_news = news.get(db, id=news_id)
    if not db_news:
        raise HTTPException(status_code=404, detail="News not found")
    news.remove(db=db, id=news_id)
    return {"message": "News deleted successfully"}

# News Section endpoints
@router.get("/news/{news_id}/sections", response_model=List[NewsSectionRead])
@cache(expire=300)
async def list_news_sections(
    news_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all sections for a news article"""
    return news_section.get_by_news(db, news_id=news_id, skip=skip, limit=limit)

@router.post("/news/{news_id}/sections", response_model=NewsSectionRead)
async def create_news_section(
    news_id: int,
    section_in: NewsSectionCreate,
    db: Session = Depends(get_db)
):
    """Create a new news section"""
    section_in.news_id = news_id
    return news_section.create(db=db, obj_in=section_in)

@router.post("/news-sections/{section_id}/image")
async def upload_news_section_image(
    section_id: int,
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload image for a news section"""
    db_section = news_section.get(db, id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="News section not found")
    
    file_url = await upload_file(file, "news/sections", request)
    news_section.update(db=db, db_obj=db_section, obj_in={"image_url": file_url})
    return {"message": "Image uploaded successfully", "url": file_url}

@router.get("/news-sections/{section_id}", response_model=NewsSectionRead)
@cache(expire=300)
async def get_news_section(
    section_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific news section by ID"""
    db_section = news_section.get(db, id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="News section not found")
    return db_section

@router.put("/news-sections/{section_id}", response_model=NewsSectionRead)
async def update_news_section(
    section_id: int,
    section_in: NewsSectionUpdate,
    db: Session = Depends(get_db)
):
    """Update a news section"""
    db_section = news_section.get(db, id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="News section not found")
    return news_section.update(db=db, db_obj=db_section, obj_in=section_in)

@router.delete("/news-sections/{section_id}")
async def delete_news_section(
    section_id: int,
    db: Session = Depends(get_db)
):
    """Delete a news section"""
    db_section = news_section.get(db, id=section_id)
    if not db_section:
        raise HTTPException(status_code=404, detail="News section not found")
    news_section.remove(db=db, id=section_id)
    return {"message": "News section deleted successfully"}
