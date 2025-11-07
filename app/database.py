from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Cấu hình Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/truong.db" 

# 2. Tạo Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # Dòng này cần thiết cho SQLite để cho phép nhiều thread kết nối
    connect_args={"check_same_thread": False} 
)

# 3. Tạo SessionLocal
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 4. Tạo Base Class cho các Models
Base = declarative_base()

# 5. Định nghĩa Hàm get_db (Đây là phần bị thiếu!)
def get_db():
    """Dependency Injector để tạo và đóng DB Session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()