from fastapi import FastAPI, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hệ thống Quản lý Sinh viên")

# Xử lý lỗi params (validate lỗi từng field)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"status": "error", "data": None, "error": exc.errors()},
    )

# Xử lý lỗi server (500)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "data": None, "error": str(exc)},
    )

# Dependency: Hàm lấy kết nối DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API tạo sinh viên mới
@app.post("/students/", response_model=schemas.StandardResponse[schemas.Student])
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = crud.create_student(db=db, student=student)
    return {"status": "success", "data": db_student, "error": None}

# API lấy danh sách sinh viên
@app.get("/students/", response_model=schemas.StandardResponse[List[schemas.Student]])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return {"status": "success", "data": students, "error": None}

@app.get("/")
def read_root():
    return {"message": "Chào mừng đến với API Quản lý Sinh viên"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)