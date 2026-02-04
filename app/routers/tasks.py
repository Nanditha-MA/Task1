from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from jose import jwt
from ..database import SessionLocal
from ..models import Task, User
from ..schemas import TaskCreate, TaskUpdate
from .auth import SECRET_KEY, ALGORITHM
from .auth import get_current_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def current_user(token=Depends(security), db: Session = Depends(get_db)):
    payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    user = db.query(User).get(payload["sub"])
    if not user:
        raise HTTPException(401)
    return user

@router.post("")
def create_task(data: TaskCreate, db: Session = Depends(get_db), user=Depends(current_user)):
    task = Task(**data.dict(), owner_id=user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("")
def list_tasks(status: str | None = None, priority: str | None = None,
               limit: int = 10, offset: int = 0,
               db: Session = Depends(get_db),
               user=Depends(current_user)):
    q = db.query(Task).filter(Task.owner_id == user.id)
    if status:
        q = q.filter(Task.status == status)
    if priority:
        q = q.filter(Task.priority == priority)
    return q.offset(offset).limit(limit).all()

@router.get("/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db), user=Depends(current_user)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(404)
    if task.owner_id != user.id:
        raise HTTPException(403)
    return task

@router.put("/{task_id}")
def update_task(task_id: str, data: TaskUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}")
def delete_task(task_id: str,
                db: Session = Depends(get_db),
                user=Depends(current_user)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(404)
    if task.owner_id != user.id:
        raise HTTPException(403)
    db.delete(task)
    db.commit()
    return {"message": "deleted"}
@router.get("")
def list_tasks(
    status: str | None = None,
    priority: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    query = db.query(Task).filter(Task.owner_id == user.id)

    if status:
        query = query.filter(Task.status == status)

    if priority:
        query = query.filter(Task.priority == priority)

    return query.offset(offset).limit(limit).all()
