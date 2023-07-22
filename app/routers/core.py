from sqlalchemy.orm import Session
from ..database import Base
from typing import Type
from fastapi import status, HTTPException


def get_object_or_404(
    session: Session, model_class: Type[Base] | str, id
) -> Type[Base]:
    object = session.query(model_class).get(id)
    if object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_class.__name__} with id={id} is not found",
        )
    else:
        return object
