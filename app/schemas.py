"""Pydantic request and response schemas."""

from pydantic import BaseModel, Field


class StudentLogin(BaseModel):
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class AdminLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
