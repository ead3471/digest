from fastapi.testclient import TestClient
from ..main import app
from pytest import fixture
from sqlalchemy.orm.session import Session
from app.models.users import Student, Teacher
from datetime import date
from app.tests.conftest import testing_session

client = TestClient(app)


@fixture()
def student_with_group(testing_session: Session):
    student = Student()
    student.name = "Иван"
    student.middle_name = "Иванович"
    student.last_name = "Иванов"
    student.passport_id = "1234 123456"
    student.birthdate = date(year=1990, day=1, month=1)
    testing_session.add(student)
    testing_session.commit()
    print("student created", student)
    yield student
    print("delete ", student)
    testing_session.delete(student)
    testing_session.commit()


@fixture()
def test_student_without_group(testing_session: Session):
    student = Student()
    student.name = "Василий"
    student.middle_name = "Васильевич"
    student.last_name = "Васильев"
    student.passport_id = "1234 123457"
    student.birthdate = date(year=1991, day=2, month=2)
    testing_session.add(student)
    testing_session.commit()


def test_create_user(testing_session: Session):
    student = Student()
    student.name = "Василий"
    student.middle_name = "Васильевич"
    student.last_name = "Васильев"
    student.passport_id = "1234 123457"
    student.birthdate = date(year=1991, day=2, month=2)
    testing_session.add(student)
    testing_session.commit()


def test_create_user_1(testing_session: Session):
    student = Student()
    student.name = "Василий"
    student.middle_name = "Васильевич"
    student.last_name = "Васильев"
    student.passport_id = "1234 123457"
    student.birthdate = date(year=1991, day=2, month=2)
    testing_session.add(student)
    testing_session.commit()


def _test_create_user_1(test_session: Session, test_student: Student):
    assert test_student.name == "Иван"
    response = client.get("/api/students")
    print(response.status_code)
    assert response.status_code == 200, response.text
    data = response.json()
