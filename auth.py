from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from ..database import SessionLocal
from ..models import User, Role
from ..schemas import UserCreate, UserLogin

SECRET_KEY = "secret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str):
    return pwd_context.hash(password[:72])


def verify_password(password: str, hashed: str):
    return pwd_context.verify(password[:72], hashed)


def create_token(user_id: str):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token=Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if data.role_id:
        role = db.query(Role).filter(Role.id == data.role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        role_id=data.role_id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"token": create_token(user.id)}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return {"token": create_token(user.id)}
def require_role(role_name: str):
    def role_checker(user=Depends(get_current_user)):
        if not user.role or user.role.name != role_name:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )
        return user
    return role_checker
