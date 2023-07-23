from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..database import Base


def get_object_or_404(
    session: Session, model_class: Type[Base] | str, id
) -> Type[Base]:
    object = session.get(model_class, id)
    if object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_class.__name__} with id={id} is not found",
        )
    else:
        return object
