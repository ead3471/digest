from fastapi import APIRouter, Depends, status, HTTPException
from ..models.users import Student, Teacher
from ..models.education import Course
from ..models.structure import Group, Department, Faculty
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.users_schemas import (
    CreateStudentSchema,
    CreateTeacherSchema,
    GetStudentSchema,
    GetTeacherSchema,
    PatchStudentSchema,
    PatchTeacherSchema,
    PutTeacherSchema,
)
from .core import get_object_or_404

router = APIRouter()


@router.post(
    "/students",
    response_model=GetStudentSchema,
    status_code=201,
    description="Creates student from the given data",
)
def create_student(
    student_data: CreateStudentSchema, db: Session = Depends(get_db)
):
    if (
        db.query(Student)
        .filter_by(passport_id=student_data.passport_id)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same passport ID already exists",
        )

    if student_data.group_id is not None:
        get_object_or_404(db, Group, student_data.group_id)

    new_student = Student(**student_data.dict())

    db.add(new_student)
    db.commit()
    return new_student


@router.get(
    "/students/{student_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=GetStudentSchema,
    description="Return data of specifed student",
)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = get_object_or_404(db, Student, student_id)
    return student


@router.get(
    "/students",
    status_code=status.HTTP_200_OK,
    response_model=list[GetStudentSchema],
    description="Get list of all students",
)
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


@router.patch(
    "/students/{student_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=GetStudentSchema,
    description="Patch student with specified data",
)
def patch_student(
    student_id: int,
    student_data: PatchStudentSchema,
    db: Session = Depends(get_db),
):
    student: Student = get_object_or_404(db, Student, student_id)

    for key, value in student_data:
        if hasattr(student, key) and value:
            setattr(student, key, value)
    db.commit()
    return student


@router.put(
    "/students/{student_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=GetStudentSchema,
    description="Replaces all student data with the given",
)
def put_student(
    student_id: int,
    student_data: PatchStudentSchema,
    db: Session = Depends(get_db),
):
    student: Student = get_object_or_404(db, Student, student_id)

    for key, value in student_data:
        if hasattr(student, key) and value:
            setattr(student, key, value)

    db.commit()
    return student


@router.delete(
    "/students/{student_id:int}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete the specifed student",
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student: Student = get_object_or_404(db, Student, student_id)

    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}


@router.post(
    "/teachers",
    status_code=status.HTTP_201_CREATED,
    response_model=GetTeacherSchema,
    description="Create teacher with specified data",
)
def create_teacher(
    teacher_data: CreateTeacherSchema, db: Session = Depends(get_db)
):
    if (
        db.query(Teacher)
        .filter_by(passport_id=teacher_data.passport_id)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Teacher with same passport id already exist",
        )

    teacher_dict = teacher_data.dict()
    courses_ids: list = teacher_dict.pop("courses")

    if courses_ids is not None:
        teacher_faculty: Faculty = get_object_or_404(
            db, Department, teacher_data.department_id
        ).faculty
        print(teacher_faculty.name)
        courses = (
            db.query(Course)
            .filter(Course.id.in_(courses_ids))
            .filter(Course.faculty == teacher_faculty)
            .all()
        )
        if len(courses_ids) != len(courses):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "One of the given courses are not exists",
                    " or not on the teacher department",
                ),
            )

        teacher_dict["courses"] = courses

    new_teacher = Teacher(**teacher_dict)

    db.add(new_teacher)
    db.commit()
    return new_teacher


@router.get(
    "/teachers/{teacher_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=GetTeacherSchema,
    description="Return data of specifed teacher",
)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher: Teacher = get_object_or_404(db, Teacher, teacher_id)
    return teacher


@router.get(
    "/teachers",
    status_code=status.HTTP_200_OK,
    response_model=list[GetTeacherSchema],
    description="Get list of all teachers",
)
def get_teachers(db: Session = Depends(get_db)):
    teachers = db.query(Teacher).all()
    return teachers


@router.patch(
    "/teachers/{teacher_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=GetTeacherSchema,
    description="Patch teacher with specified data",
)
def patch_teacher(
    teacher_id: int,
    teacher_data: PatchTeacherSchema,
    db: Session = Depends(get_db),
):
    teacher: Teacher = get_object_or_404(db, Teacher, teacher_id)

    new_teacher_faculty: Faculty = (
        teacher.department.faculty
        if teacher_data.department_id is None
        else get_object_or_404(
            db, Department, teacher_data.department_id
        ).faculty
    )

    teacher_data_dict = teacher_data.dict()

    courses = teacher_data_dict.pop("courses")

    if (
        new_teacher_faculty != teacher.department.faculty
        or courses is not None
    ):
        teacher.courses.clear()

    if courses is not None:
        new_courses = (
            db.query(Course)
            .filter(Course.id.in_(teacher_data.courses))
            .filter(Course.faculty == new_teacher_faculty)
            .all()
        )
        if len(new_courses) != len(courses):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Given corses are not presented "
                    "on the {new_teacher_faculty}"
                ),
            )

        teacher.courses = new_courses

    for key, value in teacher_data_dict.items():
        if hasattr(teacher, key) and value:
            setattr(teacher, key, value)

    db.commit()
    return teacher


@router.put(
    "/teachers/{teacher_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=GetTeacherSchema,
    description="Patch teacher with specified data",
)
def put_teacher(
    teacher_id: int,
    teacher_data: PutTeacherSchema,
    db: Session = Depends(get_db),
):
    teacher: Teacher = get_object_or_404(db, Teacher, teacher_id)

    new_teacher_faculty = get_object_or_404(
        db, Department, teacher_data.department_id
    ).faculty

    teacher_data_dict = teacher_data.dict()
    courses = teacher_data_dict.pop("courses")
    teacher.courses.clear()

    new_courses = (
        db.query(Course)
        .filter(Course.id.in_(teacher_data.courses))
        .filter(Course.faculty == new_teacher_faculty)
        .all()
    )
    if len(new_courses) != len(courses):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Given corses are not presented "
                "on the {new_teacher_faculty}"
            ),
        )

    teacher.courses = new_courses

    for key, value in teacher_data_dict.items():
        if hasattr(teacher, key) and value:
            setattr(teacher, key, value)

    db.commit()
    return teacher
