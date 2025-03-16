from sqlalchemy import text
from app.database import SessionLocal, engine
from app.models import Base

def reset_database():
    """Deletes all records from the database and resets indexes."""
    db = SessionLocal()
    
    try:
        print("Resetting database...")

        # Disable foreign key checks (For SQLite, prevents constraint errors)
        db.execute(text("PRAGMA foreign_keys = OFF;"))

        # Drop all tables
        Base.metadata.drop_all(bind=engine)

        # Recreate tables
        Base.metadata.create_all(bind=engine)

        # Re-enable foreign key checks
        db.execute(text("PRAGMA foreign_keys = ON;"))

        db.commit()
        print("Database reset successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error resetting database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_database()
