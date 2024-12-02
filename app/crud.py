from bson.objectid import ObjectId
from app.database import db  ,get_database
# from app.main import get_database

# Helper function to convert _id to id
def serialize_student(student):
    student["id"] = str(student["_id"])
    del student["_id"]
    return student

# Check if the database connection is established
def validate_db_connection():
    db = get_database()  
    print("this is db in crud.py  " , db)
    print(hasattr(db,'students'))
    print("In validation phase ")
    if db is None or not hasattr(db, 'students'):
        raise ValueError("Database connection is not established. Please ensure the database is properly initialized.")
    else:
        return db

# Create a student
async def create_student(student_data):
    print(student_data)
    
    print("going for validation ")
    db =validate_db_connection()
    print("after validation ")
    print("after validation db value ",db)
    student = await db.students.insert_one(student_data)
    return str(student.inserted_id)

# List students with filters
async def list_students(filters):
    db =validate_db_connection()
    query = {}
    if "country" in filters and filters["country"]:
        query["address.country"] = filters["country"]
    if "age" in filters and filters["age"]:
        query["age"] = {"$gte": filters["age"]}
    
    students = await db.students.find(query).to_list(100)
    return [serialize_student(s) for s in students]

# Get a student by ID
async def get_student(student_id):
    db =validate_db_connection()
    try:
        student = await db.students.find_one({"_id": ObjectId(student_id)})
        if student:
            return serialize_student(student)
        return None
    except Exception as e:
        raise ValueError(f"Failed to fetch student: {e}")

# Update a student
async def update_student(student_id, update_data):
    db =validate_db_connection()
    try:
        result = await db.students.update_one({"_id": ObjectId(student_id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise ValueError("No student found with the given ID.")
        return
    except Exception as e:
        raise ValueError(f"Failed to update student: {e}")

# Delete a student
async def delete_student(student_id):
    db =validate_db_connection()
    try:
        result = await db.students.delete_one({"_id": ObjectId(student_id)})
        if result.deleted_count == 0:
            raise ValueError("No student found with the given ID.")
        return
    except Exception as e:
        raise ValueError(f"Failed to delete student: {e}")
