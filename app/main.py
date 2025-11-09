from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, crud
from app.database import engine, get_db 

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Student Management API")

@app.get("/")
def home():
    return {"message": "Chào mừng đến Student Management API!"}


@app.post("/students", response_model=schemas.Student, status_code=201)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

class StudentListResponse(schemas.BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    data: List[schemas.Student]

@app.get("/students", response_model=StudentListResponse)
def read_students(
    page: int = Query(1, ge=1, description="Số trang, bắt đầu từ 1"),
    limit: int = Query(10, ge=1, le=100, description="Số bản ghi mỗi trang"),
    db: Session = Depends(get_db)
):
    total = db.query(models.Student).count()  # tổng số student
    students = db.query(models.Student)\
        .offset((page - 1) * limit)\
        .limit(limit)\
        .all()
    total_pages = (total + limit - 1) // limit  # tính tổng số trang

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "data": students
    }


@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student_by_id(db, student_id)
    if db_student is None:
        # Nếu không tìm thấy, ném ra lỗi 404
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student_data(student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)):
    # 1. Kiểm tra sinh viên có tồn tại không
    db_student = crud.get_student_by_id(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    # 2. Kiểm tra email mới (nếu có) có trùng với người khác không
    if student.email:
        existing_student = db.query(models.Student).filter(
            models.Student.email == student.email, 
            models.Student.id != student_id
        ).first()
        if existing_student:
            raise HTTPException(status_code=400, detail="Email already exists for another student")

    # 3. Tiến hành cập nhật
    updated_student = crud.update_student(db, student_id, student)
    return updated_student

#Xóa chi tiết học sinh theo 
@app.delete("/students/{student_id}", status_code=200)
def delete_student_data(student_id: int, db: Session = Depends(get_db)):
    deleted_student = crud.delete_student(db, student_id)
    if deleted_student is None:
        # Nếu không tìm thấy, ném ra lỗi 404
        raise HTTPException(status_code=404, detail="Student not found")
        
    return {"message": f"Student with ID {student_id} deleted successfully"}

