from typing import Annotated, Iterator
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from . import config

engine = create_engine(
    config.settings.DATABASE_URL, connect_args={'check_same_thread': False}
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


current_session = Annotated[Session, Depends(get_session)]
