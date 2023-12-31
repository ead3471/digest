from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.posts import Post, Source, Tag
from ..schemas.posts_schemas import (
    PostCreateSchema,
    PostReadSchema,
    TagReadSchema,
    SourceReadSchema,
    SourceWriteSchema,
)
from .core import get_object_or_404

router = APIRouter()


@router.get(
    "/post",
    response_model=list[PostReadSchema],
    status_code=status.HTTP_200_OK,
    description="Return all registered posts",
)
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@router.post(
    "/post",
    response_model=PostReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Create new post",
)
def create_post(post_data: PostCreateSchema, db: Session = Depends(get_db)):
    post_data_dict = post_data.dict()
    tag_ids = post_data_dict.pop("tags")
    source_id = post_data_dict.pop("source")
    source = get_object_or_404(db, Source, source_id)
    new_post = Post(**post_data_dict, source=source)
    for tag_id in tag_ids:
        tag = get_object_or_404(db, Tag, tag_id)
        new_post.tags.append(tag)
    db.add(new_post)
    db.commit()
    return new_post


@router.get(
    "/tag",
    response_model=list[TagReadSchema],
    status_code=status.HTTP_200_OK,
    description="Return all registered tags",
)
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return tags


@router.post(
    "/source",
    response_model=SourceReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Create new Source",
)
def create_source(
    source_data: SourceWriteSchema, db: Session = Depends(get_db)
):
    new_source = Source(**source_data.dict())
    db.add(new_source)
    db.commit()
    return new_source


@router.get(
    "/source",
    response_model=list[SourceReadSchema],
    status_code=status.HTTP_200_OK,
    description="Return all registered sources",
)
def get_sources(db: Session = Depends(get_db)):
    sources = db.query(Source).all()
    return sources
