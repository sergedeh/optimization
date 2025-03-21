from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Plan
from pydantic import BaseModel
from flask_pydantic import validate
from app.auth import roles_required

bp = Blueprint("plans", __name__)

class PlanRequest(BaseModel):
    name: str
    price: int
    duration_days: int

class PlanResponse(PlanRequest):
    id: int

@bp.post("/plans")
@validate()
@roles_required("admin")
def create_plan(body: PlanRequest):
    db = next(get_db())
    existing_plan = db.query(Plan).filter(Plan.name == body.name).first()
    if existing_plan:
        raise HTTPException(status_code=400, detail="Plan already exists")

    plan = Plan(name=body.name, price=body.price, duration_days=body.duration_days)
    db.add(plan)
    db.commit()
    db.refresh(plan)

    plan_response = PlanResponse(
        id=plan.id,
        name=plan.name,
        price=plan.price,
        duration_days=plan.duration_days
    )
    return {"message": "Plan created", "plan": plan_response.model_dump()}

@bp.get("/plans")
def list_plans():
    db = next(get_db())
    return db.query(Plan).all()

@bp.put("/plans/<int:plan_id>")
@roles_required("admin")
def update_plan(plan_id: int, name: str, price: int, duration_days: int):
    db = next(get_db())
    plan = db.query(Plan).get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan.name = name
    plan.price = price
    plan.duration_days = duration_days
    db.commit()
    return {"message": "Plan updated"}

@bp.delete("/plans/<int:plan_id>")
def delete_plan(plan_id: int):
    db = next(get_db())
    plan = db.query(Plan).get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    db.delete(plan)
    db.commit()
    return {"message": "Plan deleted"}
