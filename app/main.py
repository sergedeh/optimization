from app.database import Base, engine
from app import create_app

Base.metadata.create_all(bind=engine)
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
