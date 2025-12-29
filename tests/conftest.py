from typing import Iterator, NamedTuple

import pytest
from sqlmodel import SQLModel, StaticPool, create_engine, Session
from fastapi.testclient import TestClient

from app.core.security import get_password_hash
from app.main import app
from app.models.post_model import Post
from app.models.user_model import User  # type: ignore
from app.schemas.token_schema import Token
from app.services.auth_service import AuthService
from app.services.comment_service import CommentService
from app.services.post_service import PostPublicService, PostUserService
from app.services.user_service import UserService
from app.core.database import get_session


@pytest.fixture()
def session() -> Iterator[Session]:
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def client(session: Session) -> Iterator[TestClient]:
    def get_session_override() -> Session:
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


class UserFixture(NamedTuple):
    model: User
    clean_password: str


@pytest.fixture()
def user(session: Session) -> UserFixture:
    clean_pass = 'senha123'
    new_user: User = User(
        name='User', email='user@email', password=get_password_hash(clean_pass)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return UserFixture(model=new_user, clean_password=clean_pass)


@pytest.fixture()
def other_user(session: Session) -> UserFixture:
    clean_pass = 'senha123'
    new_user: User = User(
        name='User2', email='user2@email', password=get_password_hash(clean_pass)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return UserFixture(model=new_user, clean_password=clean_pass)


@pytest.fixture()
def post(user: UserFixture, session: Session) -> Post:
    new_post = Post(title='Titulo1', content='Conteudo1', user_id=user.model.id)

    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@pytest.fixture()
def other_post(other_user: UserFixture, session: Session) -> Post:
    new_post = Post(title='Titulo1', content='Conteudo1', user_id=other_user.model.id)

    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@pytest.fixture()
def token(client: TestClient, user: UserFixture) -> Token:
    response = client.post(
        '/auth/token',
        data={'username': user.model.email, 'password': user.clean_password},
    )
    return Token(**response.json())


@pytest.fixture()
def user_service(session: Session) -> UserService:
    return UserService(session)


@pytest.fixture()
def auth_service(session: Session) -> AuthService:
    return AuthService(session)


@pytest.fixture()
def post_public_service(session: Session) -> PostPublicService:
    return PostPublicService(session)


@pytest.fixture()
def post_user_service(user: UserFixture, session: Session) -> PostUserService:
    return PostUserService(user.model, session)


# Talvez tenha que implementar uma versão publica e privada de comment depois
@pytest.fixture()
def comment_service(session: Session, user: UserFixture, post: Post) -> CommentService:
    return CommentService(session, user.model, post)
