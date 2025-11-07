from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

def create_student(db: Session, student: schemas.StudentCreate):
    existing = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_students(db: Session, skip: int = 0, limit: int = 10):
    """Lấy danh sách sinh viên có phân trang."""
    return db.query(models.Student).offset(skip).limit(limit).all()


def get_student_by_id(db: Session, student_id: int):
    """Lấy sinh viên theo ID."""
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_student_count(db: Session):
    """Đếm tổng số sinh viên."""
    return db.query(models.Student).count()


def update_student(db: Session, student_id: int, update: schemas.StudentUpdate):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None

    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None

    db.delete(db_student)
    db.commit()
    return db_student