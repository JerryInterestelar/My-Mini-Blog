from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import Relationship, SQLModel, Field  # type: ignore

if TYPE_CHECKING:
    from app.models.post_model import Post


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    posts: list['Post'] = Relationship(back_populates='user')
