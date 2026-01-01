from datetime import datetime
from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentRequest(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int | None
    post_id: int
    created_at: datetime
