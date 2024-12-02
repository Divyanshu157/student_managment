from fastapi import APIRouter, HTTPException, Query
from app.models import StudentCreate, StudentUpdate, StudentResponse
from app.crud import create_student, list_students, get_student, update_student, delete_student

router = APIRouter()

# Create a new student
@router.post("/students", response_model=dict, status_code=201)
async def create_student_api(student: StudentCreate):
    student_id = await create_student(student.dict())
    return {"id": student_id}

# List students with optional filters for country and age
@router.get("/students", response_model=list[StudentResponse])
async def list_students_api(country: str = Query(None), age: int = Query(None)):
    filters = {}
    if country:
        filters["country"] = country
    if age:
        filters["age"] = age

    students = await list_students(filters)
    return students

# Get details of a specific student by ID
@router.get("/students/{id}", response_model=StudentResponse)
async def get_student_api(id: str):
    student = await get_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Update a student's details (only provided fields will be updated)
@router.patch("/students/{id}", status_code=204)
async def update_student_api(id: str, student: StudentUpdate):
    existing_student = await get_student(id)
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    await update_student(id, student.dict(exclude_unset=True))
    return

# Delete a student by ID
@router.delete("/students/{id}", status_code=200)
async def delete_student_api(id: str):
    existing_student = await get_student(id)
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    await delete_student(id)
    return {"message": "Student deleted successfully"}


