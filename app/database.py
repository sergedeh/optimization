from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from flask import g

import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./subscriptions.db")
db = SQLAlchemy()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, 
pool_size=50, max_overflow=10, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def close_db(exception=None):
    """Closes the database session at the end of each request."""
    db_session = g.pop("db", None)
    if db_session is not None:
        db_session.close()

@event.listens_for(engine, "connect")
def set_wal_mode(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")  # Enable WAL mode
    cursor.close()
