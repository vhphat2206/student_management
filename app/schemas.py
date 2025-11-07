from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from pydantic import BaseModel

class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Họ và tên đầy đủ")
    email: EmailStr = Field(..., description="Địa chỉ email")
    phone: Optional[str] = Field(None, min_length=1, max_length=20, description="Số điện thoại")
    major: str = Field(..., min_length=1, max_length=100, description="Ngành học")
    gpa: float = Field(..., ge=0.0, le=4.0, description="Điểm trung bình")

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Họ và tên đầy đủ")
    email: Optional[EmailStr] = Field(None, description="Địa chỉ email")
    phone: Optional[str] = Field(None, min_length=1, max_length=20, description="Số điện thoại")
    major: Optional[str] = Field(None, min_length=1, max_length=100, description="Ngành học")
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0, description="Điểm trung bình")

class Student(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        from_attributes = True