from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

# Schema cơ bản (dùng chung)
class StudentBase(BaseModel):
    name: str
    age: int
    class_name: str

# Schema dùng để tạo mới (Input)
class StudentCreate(StudentBase):
    pass

# Schema dùng để trả về (Output)
class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

# Schema chuẩn cho mọi phản hồi từ API
class StandardResponse(BaseModel, Generic[T]):
    status: str
    data: Optional[T] = None
    error: Optional[str] = None
