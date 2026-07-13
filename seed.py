from sqlalchemy.orm import Session

from app.auth import hash_password
from app.database import SessionLocal
from app.models import Admin, Student


def seed_database():
    db: Session = SessionLocal()

    try:
        # Create default admin
        if not db.query(Admin).filter(Admin.username == "admin").first():
            admin = Admin(
                username="admin",
                hashed_password=hash_password("admin123"),
            )
            db.add(admin)

        # Create default student
        if not db.query(Student).filter(Student.email == "student@test.com").first():
            student = Student(
                name="Test Student",
                email="student@test.com",
                hashed_password=hash_password("student123"),
            )
            db.add(student)

        db.commit()
        print("✅ Seed data added successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()