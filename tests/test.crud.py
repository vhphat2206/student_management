from fastapi.utils import create_cloned_field
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import HTTPException 
from typing import Iterator
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

from app import models, schemas, crud

TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL, 
   
    connect_args={"check_same_thread": False} 
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)

@pytest.fixture()

def db_session() -> Iterator[Session]: 
    """Tạo một session DB sạch cho mỗi test."""
    
   
    models.Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db 
    finally:
       
        db.close()
        models.Base.metadata.drop_all(bind=test_engine)
    
@pytest.fixture()
def student_data() -> schemas.StudentCreate:
    """Cung cấp dữ liệu mẫu StudentCreate hợp lệ."""
   
    return schemas.StudentCreate(
        name="Nguyên Văn Test",
        email="test.crud@example.com",
        phone="0912345678",
        major="Công nghê thông tin",
    
        gpa=3.8 

    )


def test_create_student_success(db_session: Session, student_data: schemas.StudentCreate):
    """Kiểm tra tạo sinh viên thành công và commit."""
    
    created = crud.create_student(db_session, student_data)
    db_session.commit()
    
    assert created.id is not None
    assert created.email == student_data.email
    assert created.name == student_data.name

def test_create_student_duplicate_email(db_session: Session, student_data: schemas.StudentCreate):
    """Kiểm tra tạo sinh viên trùng email (phải raise HTTPException 400)."""
    

    crud.create_student(db_session, student_data)
    db_session.commit()
    
 
    with pytest.raises(HTTPException) as excinfo:
        crud.create_student(db_session, student_data)
        
    assert excinfo.value.status_code == 400
    assert "Email already exists" in excinfo.value.detail


def test_get_student_count(db_session: Session, student_data: schemas.StudentCreate):
    """Kiểm tra get_student, get_students, và get_student_count."""
    crud.create_student(db_session, student_data)
  
    student_data_2 = student_data.model_copy(update={'email': 'test2@example.com'})
    student_2 = crud.create_student(db_session, student_data_2)
    db_session.commit()
    
    fetched_by_id = crud.get_student_by_id(db_session, student_2.id)
    assert fetched_by_id.email == "test2@example.com"
    assert crud.get_student_by_id(db_session, 999) is None
    assert crud.get_student_count(db_session) == 2
    students_list = crud.get_students(db_session, skip=1, limit=1)
    assert len(students_list) == 1

def test_update_student(db_session: Session, student_data: schemas.StudentCreate):
    """Kiểm tra cập nhật sinh viên."""
    
    created = crud.create_student(db_session, student_data)
    db_session.commit()

   
    update_data = schemas.StudentUpdate(major="Trí Tuệ Nhân Tạo", gpa=3.95) 
    
    updated = crud.update_student(db_session, created.id, update_data)

  
    assert updated.major == "Trí Tuệ Nhân Tạo"
    assert updated.gpa == 3.95
    
    
    assert crud.update_student(db_session, 999, update_data) is None

def test_delete_student(db_session: Session, student_data: schemas.StudentCreate):
    """Kiểm tra xóa sinh viên."""
    created = crud.create_student(db_session, student_data)
    db_session.commit()

    deleted = crud.delete_student(db_session, created.id)
    db_session.commit()

    assert deleted.id == created.id
    assert crud.get_student_by_id(db_session, created.id) is None
    assert crud.get_student_count(db_session) == 0
    assert crud.delete_student(db_session, 999) is None
