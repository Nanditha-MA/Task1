from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User,Role
from ..schemas import UserCreate, UserUpdate
from .auth import hash_password
from .auth import get_current_user, require_role


router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    user_obj = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role_id=data.role_id
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj
    
@router.get("")
def list_users(
    role: str | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    query = db.query(User)

    if role:
        query = query.join(Role).filter(Role.name == role)

    return query.all()



@router.get("/{user_id}")
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user_obj = db.query(User).get(user_id)

    if not user_obj:
        raise HTTPException(404)

    if user.id != user_id and user.role.name != "admin":
        raise HTTPException(403, "Forbidden")

    return user_obj


@router.put("/{user_id}")
def update_user(
    user_id: str,
    data: UserUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user_obj = db.query(User).get(user_id)

    if not user_obj:
        raise HTTPException(404)

    if user.id != user_id and user.role.name != "admin":
        raise HTTPException(403, "Forbidden")

    if data.password:
        user_obj.hashed_password = hash_password(data.password)

    if data.email:
        user_obj.email = data.email

    if data.role_id:
        user_obj.role_id = data.role_id

    db.commit()
    return user_obj

@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin"))
):
    user_obj = db.query(User).get(user_id)

    if not user_obj:
        raise HTTPException(404)

    db.delete(user_obj)
    db.commit()
    return {"message": "deleted"}
