"""Student-only course browsing and enrollment endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_student
from app.database import get_db
from app.models import Course, Enrollment, Student
from app.schemas import CourseResponse, StudentResponse
from app.encryption import decrypt

router = APIRouter(prefix="/student", tags=["Student"])


@router.get("/profile", response_model=StudentResponse)
def get_profile(
    student: Student = Depends(get_current_student),
):
    """Return the authenticated student's profile."""
    return StudentResponse(
    id=student.id,
    name=student.name,
    email=student.email,
    phone=decrypt(student.phone),
)


@router.get("/courses", response_model=list[CourseResponse])
def list_courses(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> list[Course]:
    """Return all available courses."""
    return db.query(Course).all()


@router.get("/enrolled", response_model=list[CourseResponse])
def list_enrolled_courses(
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> list[Course]:
    """Return courses enrolled by the authenticated student."""
    return (
        db.query(Course)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .filter(Enrollment.student_id == student.id)
        .all()
    )


@router.post("/enroll/{course_id}", status_code=status.HTTP_201_CREATED)
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, str]:
    """Enroll the authenticated student in a course."""
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student.id,
            Enrollment.course_id == course_id,
        )
        .first()
    )
    if enrollment is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this course",
        )

    db.add(Enrollment(student_id=student.id, course_id=course_id))
    db.commit()
    return {"message": "Enrolled in course successfully"}


@router.delete("/unenroll/{course_id}")
def unenroll_from_course(
    course_id: int,
    db: Session = Depends(get_db),
    student: Student = Depends(get_current_student),
) -> dict[str, str]:
    """Remove the authenticated student's enrollment in a course."""
    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student.id,
            Enrollment.course_id == course_id,
        )
        .first()
    )
    if enrollment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")

    db.delete(enrollment)
    db.commit()
    return {"message": "Unenrolled from course successfully"}
