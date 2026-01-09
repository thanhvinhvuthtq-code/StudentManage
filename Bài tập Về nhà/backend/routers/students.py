from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import get_db

router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/", 
    response_model=schemas.StandardResponse[schemas.Student],
    summary="Tạo hồ sơ sinh viên mới",
    description="API này nhận thông tin sinh viên mới và lưu vào cơ sở dữ liệu."
)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    Tạo một sinh viên mới.
    
    - **name**: Tên sinh viên
    - **age**: Tuổi
    - **class_name**: Tên lớp
    """
    db_student = crud.create_student(db=db, student=student)
    return 
    {
        "status": "success",
        "data": db_student, 
        "error": None
    }

@router.get(
    "/", 
    response_model=schemas.StandardResponse[List[schemas.Student]],
    summary="Lấy danh sách sinh viên",
    description="API này trả về danh sách tất cả sinh viên đang có trong hệ thống, có hỗ trợ phân trang."
)
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lấy danh sách sinh viên với phân trang.
    
    - **skip**: Số lượng bản ghi bỏ qua (mặc định 0)
    - **limit**: Số lượng bản ghi tối đa trả về (mặc định 100)
    """
    students = crud.get_students(db, skip=skip, limit=limit)
    return  
    {
        "status": "success", 
        "data": students, 
        "error": None
    }
