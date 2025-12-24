from pydantic import BaseModel

from app.schemas.post_schema import PostResponse


class UserBase(BaseModel):
    name: str
    email: str


class UserRequest(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    posts: list[PostResponse]
