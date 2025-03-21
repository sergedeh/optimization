from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from flask_pydantic import validate
from app.auth import roles_required

bp = Blueprint("users", __name__)

@bp.delete("/users/<int:user_id>")
@roles_required("admin")
def delete_user(user_id: int):
    db = next(get_db())
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
