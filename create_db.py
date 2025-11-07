from app.database import engine, Base
from app import models

print("🔄 Đang tạo bảng trong database...")
Base.metadata.create_all(bind=engine)
print("✅ Đã tạo xong bảng!")