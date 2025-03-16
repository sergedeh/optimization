from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
import jwt
import os

from app.database import SessionLocal
from app.models import User

SECRET_KEY = os.getenv("JWT_SECRET", "supersecret")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RegistrationRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
def register(request: RegistrationRequest, db: Session = Depends(get_db)):
    print(f"Request: {request}")
    hashed_password = pwd_context.hash(request.password)
    user = User(email=request.email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User registered"}

@router.post("/login")
def login(request: RegistrationRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not pwd_context.verify(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": user.email, "exp": datetime.utcnow() + timedelta(hours=1)}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
