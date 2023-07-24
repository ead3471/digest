from datetime import datetime

from pydantic import BaseModel, Field

from .users_schemas import UserBaseSchema


class ModelId(BaseModel):
    id: int = Field(description="Object id")


class TagReadSchema(BaseModel):
    id: int = Field(description="Tag id")
    name: str = Field(description="Tag name")

    class Config:
        orm_mode = True


class SourceReadSchema(BaseModel):
    id: int = Field(description="Source id")
    name: str = Field(description="Source name")

    class Config:
        orm_mode = True


class SourceWriteSchema(BaseModel):
    name: str = Field(description="Source name")

    class Config:
        orm_mode = True


class PostReadSchema(BaseModel):
    id: int = Field(description="Post id")
    text: str = Field(description="Post text")
    score: int = Field(description="Post score")
    source: SourceReadSchema = Field(description="Post source")
    tags: list[TagReadSchema] = Field(description="Post tags", default=[])
    created: datetime = Field(description="Post creation time")

    class Config:
        orm_mode = True


class PostCreateSchema(BaseModel):
    text: str = Field(description="Post text")
    score: int = Field(description="Post score")
    source: int = Field(description="Post source")
    tags: list[int] = Field(description="Post tags", default=[])
    created: datetime = Field(
        description="Post creation time", default=datetime.now()
    )

    class Config:
        orm_mode = True


class DigestReadSchema(BaseModel):
    user: UserBaseSchema = Field(description="Digest user")
    posts: list[PostReadSchema] = Field(description="Digest posts")
    created: datetime = Field(description="Digest generation time")

    class Config:
        orm_mode = True


class SubscriptionReadSchema(BaseModel):
    user_id: int = Field(description="Subscription user")
    minimum_score: int = Field(
        description="Post minimum score for adding to digest"
    )
    tags: list[TagReadSchema] = Field(description="Tags for posts searching")
    source: SourceReadSchema

    class Config:
        orm_mode = True


class SubscriptionWriteSchema(BaseModel):
    minimum_score: int = Field(
        description="Post minimum score for adding to digest"
    )
    tags: list[int] = Field(description="Tags ids for posts searching")
    source: int = Field(description="Source id")

    class Config:
        orm_mode = True
