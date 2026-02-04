

from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


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
    status: Optional[StatusEnum]
    priority: Optional[PriorityEnum] = PriorityEnum.medium


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
