from app.database import SessionLocal
from app import models

# Tạo session
db = SessionLocal()

try:
    s1 = models.Student(
        name="Nguyen Van A", email="vana@example.com",
        phone="0901234567", major="CNTT", gpa=3.5
    )
    s2 = models.Student(
        name="Tran Thi B", email="thib@example.com",
        phone="0912345678", major="Kinh tế", gpa=3.8
    )
    s3 = models.Student(
        name="Le Van C", email="vanc@example.com",
        phone="0987654321", major="Cơ khí", gpa=3.2
    )

    
    db.add_all([s1, s2, s3])
    db.commit()


    print("✅ Đã thêm 3 sinh viên vào database!")

finally:
    db.close()