from pydantic import BaseModel


class FacultySchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class DepartmentSchema(BaseModel):
    name: str
    faculty: FacultySchema

    class Config:
        orm_mode = True


class GroupSchema(BaseModel):
    name: str
    department: DepartmentSchema

    class Config:
        orm_mode = True
