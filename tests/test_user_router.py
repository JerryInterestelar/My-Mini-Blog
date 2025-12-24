import pytest  # type: ignore
from fastapi import status
from fastapi.testclient import TestClient

from app.schemas.token_schema import Token
from tests.conftest import UserFixture

r = 'Devem ser substiuidos por erros de autorização quando a verificação isOwer existir'
# @pytest.mark.skip(reason=r)
# def test_function():
#     pass

# INFO: OK tests


def test_get_users_ok(client: TestClient, user: UserFixture) -> None:
    response = client.get('/users/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json() == [
        {
            'name': user.model.name,
            'email': user.model.email,
            'id': user.model.id,
            'posts': [],
        }
    ]


def test_get_user_ok(client: TestClient, user: UserFixture) -> None:
    response = client.get('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'name': user.model.name,
        'email': user.model.email,
        'id': user.model.id,
        'posts': [],
    }


def test_create_user_ok(client: TestClient) -> None:
    response = client.post(
        '/users/',
        json={
            'name': 'user',
            'email': 'email@email',
            'password': 'senha123',
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'name': 'user',
        'email': 'email@email',
        'id': 1,
        'posts': [],
    }


def test_update_user_ok(client: TestClient, user: UserFixture, token: Token) -> None:
    response = client.put(
        f'/users/{user.model.id}',
        headers={'Authorization': f'Bearer {token.access_token}'},
        json={'name': 'User2', 'email': 'email2@email', 'password': 'senha_nova123'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'name': 'User2',
        'email': 'email2@email',
        'id': user.model.id,
        'posts': [],
    }


def test_delete_user_ok(client: TestClient, user: UserFixture, token: Token) -> None:
    response = client.delete(
        f'/users/{user.model.id}',
        headers={'Authorization': f'Bearer {token.access_token}'},
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == {'Message': 'Usuário com ID: 1 foi deletado com sucesso.'}


# INFO: ERROR Tests


def test_get_user_error_user_not_found(client: TestClient) -> None:
    response = client.get('/users/1')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_create_user_error_email_duplicado(client: TestClient, user: UserFixture):
    response = client.post(
        '/users',
        json={'name': 'User2', 'email': user.model.email, 'password': 'senha_nova123'},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Este email já está sendo usado'}


def test_update_user_error_forbidden(
    client: TestClient, user: UserFixture, other_user: UserFixture, token: Token
) -> None:
    response = client.put(
        f'/users/{other_user.model.id}',
        headers={'Authorization': f'Bearer {token.access_token}'},
        json={'name': 'User2', 'email': 'email2@email', 'password': 'senha2'},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        'detail': 'O usuário não tem permissão de alterar outro usuário'
    }


def test_delete_user_error_user_forbidden(
    client: TestClient, user: UserFixture, other_user: UserFixture, token: Token
) -> None:
    response = client.delete(
        f'/users/{other_user.model.id}',
        headers={'Authorization': f'Bearer {token.access_token}'},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        'detail': 'O usuário não tem permissão de alterar outro usuário'
    }
