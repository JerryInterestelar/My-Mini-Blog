import pytest  # type: ignore

from app.models.post_model import Post
from app.schemas.post_schema import PostRequest
from app.services.post_service import PostUserService

r = 'Implementar depois'  # type:ignore
# @pytest.mark.skip(reason=r)
# def test_function(): ...

# INFO: OK tests


def test_post_service_create_ok(post_user_service: PostUserService) -> None:
    post_request = PostRequest(title='postagem', content='conteudo da postagem')
    post_db: Post = post_user_service.create(post_request)

    assert post_db
    assert post_db.title == 'postagem'
    assert post_db.content == post_request.content


def test_post_service_list_posts_ok(post_user_service: PostUserService) -> None:
    post_request = PostRequest(title='postagem', content='conteudo da postagem')
    post_user_service.create(post_request)

    post_list = post_user_service.list_posts()
    assert len(post_list) == 1
    assert post_list[0].title == 'postagem'


def test_post_service_get_by_id_ok(post_user_service: PostUserService) -> None:
    post_request = PostRequest(title='postagem', content='conteudo da postagem')
    post_user_service.create(post_request)

    post_db = post_user_service.get_by_id(1)

    assert post_db
    assert post_db.title == 'postagem'


def test_post_service_update_ok(post_user_service: PostUserService) -> None:
    post_request = PostRequest(title='postagem', content='conteudo da postagem')
    post_db = post_user_service.create(post_request)

    assert post_db.id

    updated_post_request = PostRequest(
        title='postagem2', content='conteudo da postagem2'
    )
    updated_post_db = post_user_service.update(post_db.id, updated_post_request)

    assert updated_post_db
    assert updated_post_db.title == 'postagem2'


def test_post_service_delete_ok(post_user_service: PostUserService) -> None:
    post_request = PostRequest(title='postagem', content='conteudo da postagem')
    post_db = post_user_service.create(post_request)

    assert post_db.id

    post_user_service.delete(post_db.id)
    assert post_user_service.list_posts() == []
