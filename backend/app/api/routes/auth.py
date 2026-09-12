from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import User
from app.services.auth_service import create_access_token, get_current_user, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.get("/health")
def auth_health():
    return {"status": "ready", "mode": "jwt"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    if not payload.full_name.strip() or not email or len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="Invalid registration payload")

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return {
            "user": {"id": existing_user.id, "full_name": existing_user.full_name, "email": existing_user.email},
            "token": create_access_token(existing_user.email),
        }

    user = User(
        full_name=payload.full_name.strip(),
        email=email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "user": {"id": user.id, "full_name": user.full_name, "email": user.email},
        "token": create_access_token(user.email),
    }


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.strip().lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return {
        "user": {"id": user.id, "full_name": user.full_name, "email": user.email},
        "token": create_access_token(user.email),
    }


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "created_at": current_user.created_at,
    }
