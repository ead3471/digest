from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    id: int = Field(description="User id")
    name: str = Field(description="User name", max_length=16)

    class Config:
        orm_mode = True
