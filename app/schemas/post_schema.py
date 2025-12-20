from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostRequest(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
