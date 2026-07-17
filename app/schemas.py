"""Pydantic request and response schemas."""

from pydantic import BaseModel, ConfigDict


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


class StudentResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class StudentCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
