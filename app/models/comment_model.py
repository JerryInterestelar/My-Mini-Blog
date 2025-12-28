from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship  # type: ignore

from app.models.post_model import Post
from app.models.user_model import User


class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: int = Field(foreign_key='user.id')
    post_id: int = Field(foreign_key='post.id')
    user: Optional['User'] = Relationship(back_populates='comment')
    post: Optional['Post'] = Relationship(back_populates='comment')
