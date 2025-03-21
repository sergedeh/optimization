from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
from flask_pydantic import validate
from sqlalchemy.sql import func, text

from app.database import get_db
from app.models import Subscription, Plan
from app.auth import roles_required

class SubscribeRequest(BaseModel):
    user_id: int
    plan_id: int

bp = Blueprint("subscriptions", __name__)

@bp.post("/subscribe")
@validate()
@roles_required("user")
def subscribe(body: SubscribeRequest):
    db = next(get_db())

    plan = db.query(Plan).get(body.plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    db.execute(
        text("UPDATE subscriptions SET status='expired' WHERE user_id=:user_id AND status='active'"),
        {"user_id": body.user_id}
    )

    # Create new subscription
    new_sub = Subscription(
        user_id=body.user_id,
        plan_id=body.plan_id,
        status="active",
        start_date=func.now(),
        end_date=func.now() + timedelta(days=plan.duration_days)    
    )
    db.add(new_sub)
    db.commit()

    return jsonify({"message": "Subscription updated"}), 200

@bp.post("/subscriptions/<int:user_id>/cancel")
@roles_required("user")
def cancel_subscription(user_id: int):
    db = next(get_db())
    db.execute(text("UPDATE subscriptions SET status='canceled' WHERE user_id=:user_id AND status='active' LIMIT 1"),
               {"user_id": user_id})
    db.commit()
    return {"message": "Subscription canceled"}

@bp.get("/subscriptions/<int:user_id>/active")
@roles_required("user")
def get_active_subscriptions(user_id: int):
    db = next(get_db())
    result = db.execute(text("SELECT * FROM subscriptions WHERE user_id=:user_id AND status='active'"),
                      {"user_id": user_id}).fetchall()
    subscriptions = [dict(row._mapping) for row in result]
    return {"subscriptions": subscriptions}

@bp.get("/subscriptions/<int:user_id>/history")
@roles_required("user")
def get_subscription_history(user_id: int):
    db = next(get_db())
    result = db.execute(text("SELECT * FROM subscriptions WHERE user_id=:user_id ORDER BY start_date DESC"),
                      {"user_id": user_id}).fetchall()
    subscriptions = [dict(row._mapping) for row in result]
    return {"subscriptions": subscriptions}


@bp.delete("/subscriptions/<int:user_id>/cleanup")
@roles_required("user")
def delete_subscriptions(user_id: int):
    db = next(get_db())
    db.execute(text("DELETE FROM subscriptions WHERE user_id=:user_id"), {"user_id": user_id})
    db.commit()
    return {"message": "Test subscriptions deleted"}
