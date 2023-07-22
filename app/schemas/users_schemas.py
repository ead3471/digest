from datetime import date
from pydantic import BaseModel, Field
from typing import Optional, List
from .education_schemas import GetCourseSchema
from .core import optional

from .structure_schemas import GroupSchema, DepartmentSchema


class VisitorBaseSchema(BaseModel):
    name: str = Field(description="Visitor name", max_length=16)
    middle_name: str = Field(description="Visitor middle name", max_length=16)
    last_name: str = Field(description="Visitor last name", max_length=16)
    passport_id: str = Field(
        description="Visitor passport id", regex=r"^\d{4} \d{6}$"
    )
    birthdate: date = Field(description="Visitor birthdate")


class CreateVisitorSchema(VisitorBaseSchema):
    pass


class GetVisitorSchema(VisitorBaseSchema):
    class Config:
        orm_mode = True


class CreateStudentSchema(VisitorBaseSchema):
    group_id: Optional[int] = Field(description="Group id")


class GetStudentSchema(VisitorBaseSchema):
    id: int = Field(description="Student id")
    group: Optional[GroupSchema]

    class Config:
        orm_mode = True


class CreateTeacherSchema(VisitorBaseSchema):
    courses: Optional[List[int]] = Field(None, description="Teachers courses")
    department_id: int = Field(description="Teacher department id")


@optional
class PatchStudentSchema(CreateStudentSchema):
    pass


class PutStudentSchema(CreateStudentSchema):
    pass


@optional
class PatchTeacherSchema(CreateTeacherSchema):
    pass


class PutTeacherSchema(CreateTeacherSchema):
    pass


class GetTeacherSchema(GetVisitorSchema):
    id: int = Field(description="Teacher id")
    courses: Optional[List[GetCourseSchema]] = Field(description="Courses")
    department: DepartmentSchema


class CreateStudentCourseGradeSchema(BaseModel):
    course_id: int
    score: int
    student_id: int

    class Config:
        orm_mode = True


class PutStudentCourseGradeSchema(BaseModel):
    score: int

    class Config:
        orm_mode = True


class GetStudentCourseGradeSchema(BaseModel):
    course: GetCourseSchema
    student: GetStudentSchema
    score: int

    class Config:
        orm_mode = True
