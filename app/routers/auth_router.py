from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token_schema import Token
from app.core.dependecies import auth_service_dep
from app.core.exceptions import InvalidCredentialsError, UserEmailOrPassIncorrectError

router = APIRouter(prefix='/auth', tags=['Authetication'])


@router.post('/token')
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: auth_service_dep,
) -> Token:
    try:
        return auth_service.authenticate(form_data.username, form_data.password)
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except UserEmailOrPassIncorrectError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={'WWW-Authenticate': 'Bearer'},
        )
