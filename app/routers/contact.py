from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from ..core.db import get_db
from ..crud.contact import contact_message
from ..schemas.contact import (
    ContactMessageCreate,
    ContactMessageRead,
    ContactMessageUpdate
)

router = APIRouter()

@router.get("/contact-messages", response_model=List[ContactMessageRead])
@cache(expire=300)
async def list_contact_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """Get all contact messages with optional status filter"""
    if status:
        return contact_message.get_by_status(db, status=status, skip=skip, limit=limit)
    return contact_message.get_multi_ordered(db, skip=skip, limit=limit)

@router.post("/contact-messages", response_model=ContactMessageRead)
async def create_contact_message(
    message_in: ContactMessageCreate,
    db: Session = Depends(get_db)
):
    """Submit a new contact message"""
    return contact_message.create(db=db, obj_in=message_in)

@router.get("/contact-messages/unread", response_model=List[ContactMessageRead])
@cache(expire=60)  # Shorter cache for unread messages
async def list_unread_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all unread contact messages"""
    return contact_message.get_unread(db, skip=skip, limit=limit)

@router.get("/contact-messages/{message_id}", response_model=ContactMessageRead)
@cache(expire=300)
async def get_contact_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific contact message by ID"""
    db_message = contact_message.get(db, id=message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    return db_message

@router.put("/contact-messages/{message_id}", response_model=ContactMessageRead)
async def update_contact_message(
    message_id: int,
    message_in: ContactMessageUpdate,
    db: Session = Depends(get_db)
):
    """Update a contact message (e.g., mark as read, change status)"""
    db_message = contact_message.get(db, id=message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    return contact_message.update(db=db, db_obj=db_message, obj_in=message_in)

@router.post("/contact-messages/{message_id}/mark-read")
async def mark_message_as_read(
    message_id: int,
    db: Session = Depends(get_db)
):
    """Mark a contact message as read"""
    db_message = contact_message.get(db, id=message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    
    contact_message.update(db=db, db_obj=db_message, obj_in={"is_read": True, "status": "read"})
    return {"message": "Message marked as read"}

@router.delete("/contact-messages/{message_id}")
async def delete_contact_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    """Delete a contact message"""
    db_message = contact_message.get(db, id=message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    contact_message.remove(db=db, id=message_id)
    return {"message": "Contact message deleted successfully"}
