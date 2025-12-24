from fastapi import status
import pytest  # type: ignore
from fastapi.testclient import TestClient

from app.models.post_model import Post
from app.schemas.token_schema import Token
from tests.conftest import UserFixture


# INFO: OK Tests


def test_create_post_ok(client: TestClient, token: Token) -> None:
    response = client.post(
        '/posts',
        headers={'Authorization': f'Bearer {token.access_token}'},
        json={'title': 'Titulo1', 'content': 'Conteudo1'},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == 'Titulo1'


def test_get_posts_ok(client: TestClient, post: Post) -> None:
    # title='Titulo1', content='Conteudo1', user_id=user.model.id
    response = client.get('/posts')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]['title'] == 'Titulo1'


def test_get_post_ok(client: TestClient, post: Post) -> None:
    response = client.get(f'/posts/{post.id}')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == post.id
    assert response.json()['title'] == 'Titulo1'


def test_update_post_ok(
    client: TestClient, token: Token, user: UserFixture, post: Post
) -> None:
    response = client.put(
        f'/posts/{post.id}',
        headers={'Authorization': f'Bearer {token.access_token}'},
        json={'title': 'Titulo2', 'content': 'Conteudo2'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == 'Titulo2'


def test_delete_post_ok(
    client: TestClient, token: Token, user: UserFixture, post: Post
) -> None:
    response = client.delete(
        f'/posts/{post.id}',
        headers={'Authorization': f'Bearer {token.access_token}'},
    )
    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()['message']
        == f'Postagem de id: {user.model.id} deletada com sucesso'
    )
