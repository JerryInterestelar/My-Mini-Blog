import pytest

from app.core.exceptions import UserNotFoundError, EmailAlreadyExistsError
from app.core.security import verify_password_hash
from app.models.user_model import User
from app.schemas.user_scheme import UserRequest
from app.services.user_service import UserService

# r = 'Implementar depois'
# @pytest.mark.skip(reason=r)
# def test_function():
#     pass


def test_create_user_ok(user_service: UserService) -> None:
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    user_response: User = user_service.create(user_request)

    assert user_response.id is not None
    assert user_response.name == user_request.name
    assert user_response.password != user_request.password  # Hash Funcionou


def test_create_user_same_email_error(user_service: UserService) -> None:
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    user_service.create(user_request)

    user_request2: UserRequest = UserRequest(
        name='User2', email='user@email', password='password2'
    )
    with pytest.raises(EmailAlreadyExistsError) as error_info:
        user_service.create(user_request2)

    assert str(error_info.value) == 'Este email já está sendo usado'


def test_list_users_ok(user_service: UserService) -> None:
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    user_service.create(user_request)

    users_list: list[User] = user_service.list_users()
    user: User = users_list[0]

    assert users_list
    assert user.name in 'User'


def test_get_by_id_ok(user_service: UserService) -> None:
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    user_response: User = user_service.create(user_request)

    assert user_response.id is not None

    user_db: User | None = user_service.get_by_id(user_response.id)

    assert user_db
    assert user_db.name == user_request.name


def test_get_by_id_error(user_service: UserService) -> None:
    with pytest.raises(UserNotFoundError) as error_info:
        user_service.get_by_id(5)  # id que não existe

    assert str(error_info.value) == 'Usuário não encontrado'


def test_get_by_email_ok(user_service: UserService) -> None:
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    user_response: User = user_service.create(user_request)

    assert user_response.id is not None

    user_db: User | None = user_service.get_by_email(user_response.email)

    assert user_db
    assert user_db.email == user_request.email


def test_get_by_email_error(user_service: UserService) -> None:
    with pytest.raises(UserNotFoundError) as error_info:
        user_service.get_by_email('naoexiste@email')  # id que não existe

    assert str(error_info.value) == 'Usuário não encontrado'


def test_update_user_ok(user_service: UserService) -> None:
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    user_response: User = user_service.create(user_request).model_copy()

    assert user_response.id is not None

    updated_user_request: UserRequest = UserRequest(
        name='User2', email='user2@email', password='password2'
    )
    updated_user_response: User = user_service.update(
        user_response.id, updated_user_request
    )

    assert updated_user_response
    assert updated_user_response.name == 'User2'
    assert verify_password_hash('password2', updated_user_response.password)


def test_update_user_error(user_service: UserService) -> None:
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    with pytest.raises(UserNotFoundError) as error_info:
        user_service.update(99, user_request)  # id que não existe

    assert str(error_info.value) == 'Usuário não encontrado'


def test_delete_user_ok(user_service: UserService) -> None:
    user_request: UserRequest = UserRequest(
        name='User', email='user@email', password='password'
    )
    user_response: User = user_service.create(user_request).model_copy()

    assert user_response.id is not None

    user_service.delete(user_response.id)

    assert user_service.list_users() == []


def test_delete_user_error(user_service: UserService) -> None:
    with pytest.raises(UserNotFoundError) as error_info:
        user_service.delete(99)  # id que não existe

    assert str(error_info.value) == 'Usuário não encontrado'
