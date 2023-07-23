from fastapi.testclient import TestClient
from ..main import app
from pytest import fixture
from sqlalchemy.orm.session import Session
from datetime import date
from app.tests.conftest import testing_session
from models.users import User
from models.posts import Post, Source, Tag, Subscription, Digest

client = TestClient(app)


@fixture()
def posts(testing_session: Session):
    tags = [Tag("1"), Tag("2"), Tag("3")]
    for tag in tags:
        testing_session.add(tag)


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
