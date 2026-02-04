import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

def uid():
    return str(uuid.uuid4())

class Role(Base):
    __tablename__ = "roles"
    id = Column(String, primary_key=True, default=uid)
    name = Column(String, unique=True)

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(String, primary_key=True, default=uid)
    name = Column(String, unique=True)

class RoleHasPermission(Base):
    __tablename__ = "role_permissions"
    role_id = Column(String, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(String, ForeignKey("permissions.id"), primary_key=True)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=uid)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role_id = Column(String, ForeignKey("roles.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role")
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=uid)
    title = Column(String)
    description = Column(String)
    status = Column(String, default="pending")
    priority = Column(String, default="medium")
    owner_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="tasks")
