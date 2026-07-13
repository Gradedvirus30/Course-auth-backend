"""Password hashing and JWT helpers."""

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.database import get_db
from app.models import Admin, Student

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

INVALID_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
ADMIN_REQUIRED_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Administrator access required",
)


def hash_password(password: str) -> str:
    """Return a bcrypt hash for a plaintext password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return whether a plaintext password matches its stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """Create a signed JWT with an expiration claim."""
    payload = data.copy()
    expires_at = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload.update({"exp": expires_at})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decode a valid JWT, returning ``None`` for an invalid or expired token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def _get_token_subject(token: str, expected_role: str) -> int:
    """Validate a token's subject and role, returning the database identifier."""
    payload = decode_access_token(token)
    if payload is None:
        raise INVALID_TOKEN_EXCEPTION

    subject = payload.get("sub")
    if payload.get("role") != expected_role:
        if expected_role == "admin":
            raise ADMIN_REQUIRED_EXCEPTION
        raise INVALID_TOKEN_EXCEPTION

    try:
        return int(subject)
    except (TypeError, ValueError):
        raise INVALID_TOKEN_EXCEPTION


def get_current_student(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Student:
    """Return the authenticated student represented by the Bearer token."""
    student_id = _get_token_subject(token, expected_role="student")
    student = db.get(Student, student_id)
    if student is None:
        raise INVALID_TOKEN_EXCEPTION
    return student


def get_current_admin(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Admin:
    """Return the authenticated admin; reject student and malformed tokens."""
    admin_id = _get_token_subject(token, expected_role="admin")
    admin = db.get(Admin, admin_id)
    if admin is None:
        raise INVALID_TOKEN_EXCEPTION
    return admin
