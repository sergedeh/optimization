from fastapi import FastAPI
from app.database import Base, engine
from app.routers import subscriptions
from app.auth import router as auth_router
from app.routers import plans, users

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(subscriptions.router, prefix="/subscriptions")
app.include_router(plans.router, prefix="/plans")
app.include_router(users.router, prefix="/users")
