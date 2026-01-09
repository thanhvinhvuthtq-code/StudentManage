from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from . import models
from .database import engine
from .routers import students

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hệ thống Quản lý Sinh viên",
    description="API cung cấp các chức năng quản lý sinh viên bao gồm Thêm, Sửa, Xóa và Tìm kiếm.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include routers
app.include_router(students.router)

# Xử lý lỗi params (validate lỗi từng field)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=
        {
            "status": "error", 
            "data": None, 
            "error": exc.errors()
        },
    )

# Xử lý lỗi server (500)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=
        {
            "status": "error", 
            "data": None, 
            "error": str(exc)
        },
    )

@app.get("/")
def read_root():
    return {"message": "Chào mừng đến với API Quản lý Sinh viên"}
