from pydantic import BaseModel
from typing import Optional
import datetime

class StudentCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    major: str
    gpa: float

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    major: Optional[str] = None
    gpa: Optional[float] = None

class Student(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    major: str
    gpa: float
    created_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True