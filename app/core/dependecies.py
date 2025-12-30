import jwt
from jwt import InvalidTokenError
from typing import Annotated, cast, Any
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.database import get_session
from app.core.config import settings
from app.core.exceptions import InvalidCredentialsError
from app.models.user_model import User
from app.schemas.token_schema import TokenData
from app.services.auth_service import AuthService
from app.services.post_service import PostPublicService, PostUserService
from app.services.user_service import UserService


oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

session_dep = Annotated[Session, Depends(get_session)]
token_dep = Annotated[str, Depends(oauth_scheme)]


def get_current_user(token: token_dep, session: session_dep) -> User:
    try:
        payload_raw = jwt.decode(  # type: ignore
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        payload = cast(dict[str, Any], payload_raw)
        email: str | None = payload.get('sub')
        if email is None:
            raise InvalidCredentialsError('Não foi possível validar as credenciais')
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise InvalidCredentialsError('Não foi possível validar as credenciais')

    user_service = UserService(session)
    user_db = user_service.get_by_email(token_data.email)
    return user_db


def get_user_service(session: session_dep) -> UserService:
    return UserService(session)


def get_auth_service(session: session_dep) -> AuthService:
    return AuthService(session)


user_service_dep = Annotated[UserService, Depends(get_user_service)]
auth_service_dep = Annotated[AuthService, Depends(get_auth_service)]

current_user_dep = Annotated[User, Depends(get_current_user)]


def get_post_service(session: session_dep) -> PostPublicService:
    return PostPublicService(session)


def get_user_post_service(
    user: current_user_dep, session: session_dep
) -> PostUserService:
    return PostUserService(user, session)


post_public_service_dep = Annotated[PostUserService, Depends(get_post_service)]
post_user_service_dep = Annotated[PostUserService, Depends(get_user_post_service)]
