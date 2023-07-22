from app.tests.conftest import testing_session

from sqlalchemy.orm.session import Session
from pytest import fixture
from app.models.structure import Group, Faculty, Department
from typing import NamedTuple, Generator



@fixture()
def student(testing_session:Session)