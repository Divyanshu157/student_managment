from fastapi import APIRouter, HTTPException, Query
from app.models import StudentCreate, StudentUpdate, StudentResponse
from app.crud import create_student, list_students, get_student, update_student, delete_student

router = APIRouter()



@router.post("/students", response_model=dict, status_code=201)
async def create_student_api(student: StudentCreate):
    student_id = await create_student(student.dict())
    return {"id": student_id}

@router.get("/students", response_model=list[StudentResponse])
async def list_students_api(country: str = Query(None), age: int = Query(None)):
    students = await list_students({"country": country, "age": age})
    return students

@router.get("/students/{id}", response_model=StudentResponse)
async def get_student_api(id: str):
    student = await get_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.patch("/students/{id}", status_code=204)
async def update_student_api(id: str, student: StudentUpdate):
    await update_student(id, student.dict(exclude_unset=True))
    return

@router.delete("/students/{id}", status_code=200)
async def delete_student_api(id: str):
    await delete_student(id)
    return {"message": "Student deleted successfully"}
