from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers.auth import router as auth_router
from app.routers import admin
from app.routers import student

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management Backend",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(admin.router)
app.include_router(student.router)

@app.get("/")
def root():
    return {"message": "Course Management Backend is running!"}
