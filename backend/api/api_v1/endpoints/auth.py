from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.backend.deps import get_db
from app.backend.crud import crud
from app.backend.core.security import verify_password, create_access_token, hash_password
from app.backend.schemas.schemas import Token, UserCreate, UserRead
from datetime import timedelta
from app.backend.core.config import get_settings

router = APIRouter(prefix="/api/auth", tags=["auth"])
settings = get_settings()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm has username field; we use it as email
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRES_MINUTES)
    token = create_access_token({"user_id": user.id, "email": user.email}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, name=user_in.name, email=user_in.email, password_hash=hash_password(user_in.password), is_active=user_in.is_active)
    return user
