from app.tests.conftest import testing_session

from sqlalchemy.orm.session import Session
from pytest import fixture
from app.models.posts import Group, Faculty, Department
from typing import NamedTuple, Generator


class UnivercityStructure(NamedTuple):
    faculty: Faculty
    department: Department
    group: Group


@fixture()
def univercity_structure(
    testing_session: Session,
) -> Generator[UnivercityStructure, None, None]:
    new_faculty = Faculty(name="Some faculty name")
    new_department = Department(name="Some department", faculty=new_faculty)
    new_group = Group(name="Some group", department=new_department)
    testing_session.add(new_faculty)
    testing_session.add(new_department)
    testing_session.add(new_group)
    testing_session.commit()

    yield UnivercityStructure(new_faculty, new_department, new_group)
    testing_session.delete(new_group)
    testing_session.delete(new_department)
    testing_session.delete(new_faculty)
