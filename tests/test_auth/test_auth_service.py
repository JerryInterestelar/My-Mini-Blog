import pytest

from app.core.exceptions import UserEmailOrPassIncorrectError
from app.schemas.token_schema import Token
from app.services.auth_service import AuthService
from app.schemas.user_scheme import UserRequest
from app.services.user_service import UserService

# r = 'Implementar depois'
# @pytest.mark.skip(reason=r)
# def test_function():
#     pass


def test_autenticate_ok(auth_service: AuthService, user_service: UserService) -> None:
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    user_service.create(user_request)

    response: Token = auth_service.authenticate('user@email', 'password')
    assert response is not None
    assert response.token_type == 'bearer'


def test_autenticate_error_invalid_email(
    auth_service: AuthService, user_service: UserService
):
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    user_service.create(user_request)

    with pytest.raises(UserEmailOrPassIncorrectError) as error_info:
        auth_service.authenticate('invalid@email', 'password')

    assert str(error_info.value) == 'Email ou Senha Incorretos'


def test_autenticate_error_invalid_password(
    auth_service: AuthService, user_service: UserService
):
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    user_service.create(user_request)

    with pytest.raises(UserEmailOrPassIncorrectError) as error_info:
        auth_service.authenticate('user@email', 'not_the_password')

    assert str(error_info.value) == 'Email ou Senha Incorretos'
