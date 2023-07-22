from fastapi import APIRouter, Depends

from .users import Student

from ..models.education import Course, CourseGrade
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.users_schemas import (
    CreateStudentCourseGradeSchema,
    GetStudentCourseGradeSchema,
    PutStudentCourseGradeSchema,
)

from ..schemas.users_schemas import GetStudentSchema
from ..schemas.education_schemas import CreateCourseSchema, GetCourseSchema

from .core import get_object_or_404

from ..models.structure import Faculty

router = APIRouter()


@router.post(
    "/courses",
    response_model=GetCourseSchema,
    status_code=201,
    description="Creates new course on faculty",
)
def create_course(
    course_data: CreateCourseSchema, db: Session = Depends(get_db)
):
    get_object_or_404(db, Faculty, course_data.faculty_id)

    new_course = Course(**course_data.dict())
    db.add(new_course)
    db.commit()

    return new_course


@router.get(
    "/courses/{course_id}",
    response_model=GetCourseSchema,
    status_code=201,
    description="Get course by id",
)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = get_object_or_404(db, Course, course_id)
    return course


@router.get(
    "/courses/{course_id}/students/",
    response_model=list[GetStudentSchema],
    status_code=201,
    description="Get all course students",
)
def get_course_students(course_id: int, db: Session = Depends(get_db)):
    course: Course = get_object_or_404(db, Course, course_id)
    return course.students


@router.post(
    "/grades",
    response_model=GetStudentCourseGradeSchema,
    status_code=201,
    description="Creates new student course score",
)
def create_grade(
    grade_data: CreateStudentCourseGradeSchema, db: Session = Depends(get_db)
):
    get_object_or_404(db, Student, grade_data.student_id)
    get_object_or_404(db, Course, grade_data.course_id)
    new_grade = CourseGrade(**grade_data.dict())
    db.add(new_grade)
    db.commit()
    return new_grade


@router.put(
    "/grades/{grade_id:int}",
    response_model=GetStudentCourseGradeSchema,
    description="Update student course score ",
)
def put_grade(
    grade_id: int,
    grade_data: PutStudentCourseGradeSchema,
    db: Session = Depends(get_db),
):
    grade: CourseGrade = get_object_or_404(db, CourseGrade, grade_id)
    grade.score = grade_data.score
    db.commit()
    return grade
