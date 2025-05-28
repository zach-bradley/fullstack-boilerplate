from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    email: EmailStr

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None