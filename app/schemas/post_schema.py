from datetime import datetime
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostRequest(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    user_id: int  # Pode ser necessário implementar isso melhor depois
    created_at: datetime
    updated_at: datetime
