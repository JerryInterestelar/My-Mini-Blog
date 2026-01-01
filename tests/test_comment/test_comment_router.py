from fastapi.testclient import TestClient
from fastapi import status

from app.schemas.token_schema import Token
from app.models.comment_model import Comment


def test_update_comment_ok(client: TestClient, token: Token, comment: Comment) -> None:
    response = client.put(
        f'/comments/{comment.id}',
        headers={'Authorization': f'Bearer {token.access_token}'},
        json={'content': 'Conteudo2'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['content'] == 'Conteudo2'


def test_delete_comment_ok(client: TestClient, token: Token, comment: Comment) -> None:
    response = client.delete(
        f'/comments/{comment.id}',
        headers={'Authorization': f'Bearer {token.access_token}'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()['message']
        == f'Comentário de id: {comment.id} deletado com sucesso'
    )
