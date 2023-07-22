from pydantic import BaseModel, Field
from .structure_schemas import FacultySchema


class CreateCourseSchema(BaseModel):
    name: str = Field(description="Course name")
    faculty_id: int = Field(description="Faculty id")

    class Config:
        orm_mode = True


class GetCourseSchema(BaseModel):
    name: str = Field(description="Course name")
    faculty: FacultySchema

    class Config:
        orm_mode = True
