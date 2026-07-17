"""Seed the database with sample admins, students and courses."""

from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.models import Admin, Course, Enrollment, Student

# Recreate database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# -------------------------
# Admin
# -------------------------

admin = Admin(
    username="admin",
    phone="9123456789",
    hashed_password=hash_password("admin123"),
)

db.add(admin)

# -------------------------
# Students
# -------------------------

students = [
    Student(
        name="Alice Johnson",
        email="alice@test.com",
	phone="8956814477",
        hashed_password=hash_password("alice123"),
    ),
    Student(
        name="Bob Smith",
        email="bob@test.com",
	phone="9740588201",
        hashed_password=hash_password("bob123"),
    ),
    Student(
        name="Charlie Brown",
        email="charlie@test.com",
	phone="9941230056",
        hashed_password=hash_password("charlie123"),
    ),
]

db.add_all(students)

# -------------------------
# Courses
# -------------------------

courses = [
    Course(
        course_name="Artificial Intelligence",
        description="Introduction to AI concepts and machine learning.",
    ),
    Course(
        course_name="Data Structures",
        description="Stacks, queues, trees, graphs and algorithms.",
    ),
    Course(
        course_name="Cloud Computing",
        description="Fundamentals of cloud platforms and deployment.",
    ),
    Course(
        course_name="Database Systems",
        description="SQL, normalization and database design.",
    ),
]

db.add_all(courses)

db.commit()

# Refresh so IDs are available
for student in students:
    db.refresh(student)

for course in courses:
    db.refresh(course)

# -------------------------
# Enrollments
# -------------------------

enrollments = [
    Enrollment(
        student_id=students[0].id,
        course_id=courses[0].id,
    ),
    Enrollment(
        student_id=students[0].id,
        course_id=courses[3].id,
    ),
    Enrollment(
        student_id=students[1].id,
        course_id=courses[0].id,
    ),
    Enrollment(
        student_id=students[1].id,
        course_id=courses[2].id,
    ),
    Enrollment(
        student_id=students[2].id,
        course_id=courses[1].id,
    ),
]

db.add_all(enrollments)
db.commit()

db.close()

print("✅ Database seeded successfully.")