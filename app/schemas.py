from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role_id: Optional[str]

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    role_id: Optional[str]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    status: Optional[str]
    priority: Optional[str]

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

