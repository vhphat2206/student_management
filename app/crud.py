from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas
# thêm sinh viên mới 
# existing lệnh dùng để kiểm tra các mail bị trùng nhau 
def create_student(db: Session, student: schemas.StudentCreate):
    existing = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")# nếu mail bị trùng: hiện lỗi 400(trùng dữ liệu), detail: nội dung lỗi(email đã tồn tại) 

    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)# refresh: là hàm dùng để trả về lấy lại thông tin mới nhất
    return db_student

# get_studnets: lấy sinh viên
# Skip: bỏ qua vị trí số 0 
# limit: giới hạn tối đa
# Session: đối tượng để get
# return:trả về kết quả, all: lấy tất cả 
def get_students(db: Session, skip: int = 0, limit: int = 10):
    """Lấy danh sách sinh viên có phân trang."""
    return db.query(models.Student).offset(skip).limit(limit).all()

# get_student_by_id, student_id: id của sinh viên
# first(): lấy kết quả đầu tiên
def get_student_by_id(db: Session, student_id: int):
    """Lấy sinh viên theo ID."""
    return db.query(models.Student).filter(models.Student.id == student_id).first()

# get_student_count: Đếm tổng số sinh viên
# đùng count() để trả vè tổng số sinh viên
def get_student_count(db: Session):
    """Đếm tổng số sinh viên."""
    return db.query(models.Student).count()

# update_student: cập nhật thông tin sinh viên
# schemas.StudentUpdate: lấy cấu trúc cập nhập học sinh từ bảng schemas
# return None: trả về kết quả nếu không tìm thấy
def update_student(db: Session, student_id: int, update: schemas.StudentUpdate):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None

    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(db_student, key, value)# Cập nhật các trường được chuyển vào 
    db.commit()# Lưu kết quả 
    db.refresh(db_student)# refresh dùng để lấy lại thông tin mới nhất
    return db_student# trả về các đối tượng đã đc cập nhật

# delete_student: xóa sinh viên
def delete_student(db: Session, student_id: int):
    db_student = get_student_by_id(db, student_id)
    if not db_student:
        return None

    db.delete(db_student)
    db.commit()
    return db_student
