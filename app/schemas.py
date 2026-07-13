"""Pydantic request and response schemas."""

from pydantic import BaseModel, ConfigDict, Field


class StudentLogin(BaseModel):
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class AdminLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CourseCreate(BaseModel):
    course_name: str
    description: str


class CourseUpdate(BaseModel):
    course_name: str | None = None
    description: str | None = None


class CourseResponse(BaseModel):
    id: int
    course_name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
