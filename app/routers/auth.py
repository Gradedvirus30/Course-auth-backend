"""Authentication endpoints for students and administrators."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, verify_password
from app.database import get_db
from app.models import Admin, Student
from app.schemas import AdminLogin, StudentLogin, Token

router = APIRouter(tags=["authentication"])

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/student/login", response_model=Token)
def student_login(credentials: StudentLogin, db: Session = Depends(get_db)) -> Token:
    """Authenticate a student by email and return an access token."""
    student = db.query(Student).filter(Student.email == credentials.email).first()
    if student is None or not verify_password(
        credentials.password, student.hashed_password
    ):
        raise INVALID_CREDENTIALS

    token = create_access_token({"sub": str(student.id), "role": "student"})
    return Token(access_token=token)


@router.post("/admin/login", response_model=Token)
def admin_login(credentials: AdminLogin, db: Session = Depends(get_db)) -> Token:
    """Authenticate an administrator by username and return an access token."""
    admin = db.query(Admin).filter(Admin.username == credentials.username).first()
    if admin is None or not verify_password(
        credentials.password, admin.hashed_password
    ):
        raise INVALID_CREDENTIALS

    token = create_access_token({"sub": str(admin.id), "role": "admin"})
    return Token(access_token=token)
