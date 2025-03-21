from flask import Blueprint, current_app, request, jsonify
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from flask_pydantic import validate
from functools import wraps

import os
from flask_jwt_extended import get_jwt,create_access_token, jwt_required, get_jwt_identity, JWTManager

from app.database import get_db
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def roles_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):

            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return jsonify({"error": f"Unauthorized, roles allowed: {', '.join(allowed_roles)}"}), 403

            return f(*args, **kwargs)

        return wrapper
    return decorator

bp = Blueprint("auth", __name__)

class LoginRequest(BaseModel):
    email: str
    password: str

class RegistrationRequest(LoginRequest):
    role: str


@bp.post("/register")
@validate()
def register(body: RegistrationRequest):
    db = next(get_db())
    hashed_password = pwd_context.hash(body.password)
    user = User(email=body.email, password_hash=hashed_password, role= body.role)
    db.add(user)
    db.commit()
    return {"message": "User registered"}

@bp.post("/login")
@validate()
def login(body: LoginRequest):
    db = next(get_db())
    user = db.query(User).filter(User.email == body.email).first()
    if not user or not pwd_context.verify(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(identity=user.email, additional_claims={"role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}
