from flask import Flask
from app.database import db, close_db
from app.config import Config
from app.routers import subscriptions
from app.routers import plans
from app.routers import users
from app import auth
from flask_jwt_extended import JWTManager
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)
    app.config["SECRET_KEY"] = os.getenv("JWT_SECRET", "supersecret")

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(subscriptions.bp, url_prefix="/subscriptions")
    app.register_blueprint(plans.bp, url_prefix="/plans")
    app.register_blueprint(users.bp, url_prefix="/users")
    app.register_blueprint(auth.bp, url_prefix="/auth")

    app.teardown_request(close_db)

    return app
