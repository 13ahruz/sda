from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional

class ContactMessageBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: constr(pattern=r"^[0-9+\-\s()]{7,20}$")
    email: EmailStr
    message: Optional[str] = None
    cv_url: Optional[str] = None
    is_read: bool = False
    status: str = "new"

class ContactMessageCreate(ContactMessageBase):
    pass

class ContactMessageUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[constr(pattern=r"^[0-9+\-\s()]{7,20}$")] = None
    email: Optional[EmailStr] = None
    message: Optional[str] = None
    cv_url: Optional[str] = None
    is_read: Optional[bool] = None
    status: Optional[str] = None

class ContactMessageRead(ContactMessageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
