"""Authentication endpoints for students and administrators."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    verify_password,
    hash_password,
)
from app.database import get_db
from app.models import Admin, Student
from app.schemas import Token, StudentCreate
from app.encryption import encrypt

router = APIRouter(prefix="/auth", tags=["authentication"])

INVALID_CREDENTIALS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post(
    "/student/register",
    status_code=status.HTTP_201_CREATED,
)
def register_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
):
    """Register a new student."""

    existing_student = (
        db.query(Student)
        .filter(Student.email == student_data.email)
        .first()
    )

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    student = Student(
        name=student_data.name,
        email=student_data.email,
        phone=encrypt(student_data.phone),
        hashed_password=hash_password(student_data.password),
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {"message": "Student registered successfully"}


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """Authenticate an administrator or student and return an access token."""
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()
    if admin is not None and verify_password(form_data.password, admin.hashed_password):
        token = create_access_token({"sub": str(admin.id), "role": "admin"})
        return Token(access_token=token)

    student = db.query(Student).filter(Student.email == form_data.username).first()
    if student is not None and verify_password(
        form_data.password, student.hashed_password
    ):
        token = create_access_token({"sub": str(student.id), "role": "student"})
        return Token(access_token=token)

    raise INVALID_CREDENTIALS

