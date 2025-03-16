from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.database import SessionLocal
from app.models import Subscription, Plan
from app.auth import SECRET_KEY
import jwt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SubscribeRequest(BaseModel):
    user_id: int
    plan_id: int

@router.post("/subscribe")
def subscribe(request: SubscribeRequest, db: Session = Depends(get_db)):

    print(f"Received request: {request}")

    plan = db.query(Plan).get(request.plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    db.execute(text("UPDATE subscriptions SET status='expired' WHERE user_id=:user_id AND status='active'"),
               {"user_id": request.user_id})
    
    new_sub = Subscription(
        user_id= request.user_id,
        plan_id= request.plan_id,
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=plan.duration_days),
        status="active"
    )
    
    db.add(new_sub)
    db.commit()
    return {"message": "Subscription updated"}

@router.post("/subscriptions/{user_id}/cancel")
def cancel_subscription(user_id: int, db: Session = Depends(get_db)):
    db.execute(text("UPDATE subscriptions SET status='canceled' WHERE user_id=:user_id AND status='active'"),
               {"user_id": user_id})
    db.commit()
    return {"message": "Subscription canceled"}

@router.get("/subscriptions/{user_id}/active")
def get_active_subscriptions(user_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM subscriptions WHERE user_id=:user_id AND status='active'"),
                      {"user_id": user_id}).fetchall()
    subscriptions = [dict(row._mapping) for row in result]
    return {"subscriptions": subscriptions}

@router.get("/subscriptions/{user_id}/history")
def get_subscription_history(user_id: int, db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM subscriptions WHERE user_id=:user_id ORDER BY start_date DESC"),
                      {"user_id": user_id}).fetchall()
    subscriptions = [dict(row._mapping) for row in result]
    return {"subscriptions": subscriptions}


@router.delete("/subscriptions/{user_id}/cleanup")
def delete_subscriptions(user_id: int, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM subscriptions WHERE user_id=:user_id"), {"user_id": user_id})
    db.commit()
    return {"message": "Test subscriptions deleted"}
