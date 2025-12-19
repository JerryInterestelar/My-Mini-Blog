from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserRequest(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
