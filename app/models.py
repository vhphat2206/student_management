from sqlalchemy import Column, Integer, String, Float, DateTime, func
from .database import Base 

class Student(Base):
    __tablename__ = "students"  

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(100), nullable=False)           
    email = Column(String(100), nullable=False, unique=True)  
    phone = Column(String(20), nullable=True)           
    major = Column(String(100), nullable=False)       
    gpa = Column(Float, nullable=False)                 
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 