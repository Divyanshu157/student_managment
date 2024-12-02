from bson.objectid import ObjectId
from app.database import db

# Helper function to convert _id to id
def serialize_student(student):
    student["id"] = str(student["_id"])
    del student["_id"]
    return student

# Create a student
async def create_student(student_data):
    student = await db.students.insert_one(student_data)
    return str(student.inserted_id)

# List students with filters
async def list_students(filters):
    query = {}
    if "country" in filters and filters["country"]:
        query["address.country"] = filters["country"]
    if "age" in filters and filters["age"]:
        query["age"] = {"$gte": filters["age"]}
    
    students = await db.students.find(query).to_list(100)
    return [serialize_student(s) for s in students]

# Get a student by ID
async def get_student(student_id):
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if student:
        return serialize_student(student)
    return None

# Update a student
async def update_student(student_id, update_data):
    await db.students.update_one({"_id": ObjectId(student_id)}, {"$set": update_data})
    return

# Delete a student
async def delete_student(student_id):
    await db.students.delete_one({"_id": ObjectId(student_id)})
    return
