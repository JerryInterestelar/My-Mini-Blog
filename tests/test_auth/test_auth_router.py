from fastapi import status

# import pytest
from fastapi.testclient import TestClient

from tests.conftest import UserFixture


r = 'Implementado dps'
# @pytest.mark.skip(reason=r)
# def test_function() -> None:
#     pass


def test_login_ok(client: TestClient, user: UserFixture) -> None:
    response = client.post(
        '/auth/token',
        data={
            'username': user.model.email,
            'password': user.clean_password,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['token_type'] == 'bearer'


def test_login_error_wrong_email(client: TestClient, user: UserFixture) -> None:
    response = client.post(
        '/auth/token',
        data={
            'username': 'Email errado',
            'password': user.clean_password,
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_error_wrong_password(client: TestClient, user: UserFixture) -> None:
    response = client.post(
        '/auth/token',
        data={
            'username': user.model.email,
            'password': 'senha errada',
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
