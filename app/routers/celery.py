from ..tasks.tasks import test_task
from fastapi import APIRouter

from fastapi import status

router = APIRouter("Celery tasks")


@router.get("/create_test_task", status_code=status.HTTP_200_OK,)
def submit_test_task():
    
