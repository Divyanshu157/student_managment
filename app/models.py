from pydantic import BaseModel, Field
from typing import Optional

# Address model representing the address structure
class Address(BaseModel):
    city: str
    country: str

# StudentCreate model for creating a student
class StudentCreate(BaseModel):
    name: str
    age: int
    address: Address

# StudentUpdate model for updating a student's data, where all fields are optional
class StudentUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]
    address: Optional[Address]

# StudentResponse model for returning the student data in response
class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    address: Address

    # Pydantic's method to serialize the response model with an ObjectId field
    class Config:
        orm_mode = True  # Ensures that Pydantic models can work with non-dict data like MongoDB ObjectId
