from fastapi import FastAPI

from app.database import Base, engine
from app import models

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management Backend",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Course Management Backend is running!"}