from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Plan
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PlanRequest(BaseModel):
    name: str
    price: int
    duration_days: int

@router.post("/plans")
def create_plan(request: PlanRequest, db: Session = Depends(get_db)):
    existing_plan = db.query(Plan).filter(Plan.name == request.name).first()
    if existing_plan:
        raise HTTPException(status_code=400, detail="Plan already exists")

    plan = Plan(name=request.name, price=request.price, duration_days=request.duration_days)
    db.add(plan)
    db.commit()
    return {"message": "Plan created", "plan": plan}

@router.get("/plans")
def list_plans(db: Session = Depends(get_db)):
    return db.query(Plan).all()

@router.put("/plans/{plan_id}")
def update_plan(plan_id: int, name: str, price: int, duration_days: int, db: Session = Depends(get_db)):
    plan = db.query(Plan).get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan.name = name
    plan.price = price
    plan.duration_days = duration_days
    db.commit()
    return {"message": "Plan updated"}

@router.delete("/plans/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(Plan).get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    db.delete(plan)
    db.commit()
    return {"message": "Plan deleted"}
