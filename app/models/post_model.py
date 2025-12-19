from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, SQLModel, Field  # type: ignore
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.user_model import User


class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={'onupdate': lambda: datetime.now(timezone.utc)},
    )
    user_id: int | None = Field(default=None, foreign_key='user.id')
    user: Optional['User'] = Relationship(back_populates='posts')
