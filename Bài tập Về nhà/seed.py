from api.database import SessionLocal
from api.models import Student

def seed_data():
    db = SessionLocal()
    
    # Kiểm tra xem đã có dữ liệu chưa để tránh trùng lặp
    if db.query(Student).count() > 0:
        print("Database already has data. Skipping seed.")
        db.close()
        return

    students = [
        Student(name="Nguyễn Văn A", age=20, class_name="CNTT K15"),
        Student(name="Trần Thị B", age=21, class_name="KTPM K14"),
        Student(name="Lê Văn C", age=22, class_name="HTTT K13"),
        Student(name="Phạm Thị D", age=20, class_name="CNTT K15"),
        Student(name="Hoàng Văn E", age=19, class_name="KHMT K16")
    ]

    try:
        db.add_all(students)
        db.commit()
        print("Successfully seeded 5 students!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()

