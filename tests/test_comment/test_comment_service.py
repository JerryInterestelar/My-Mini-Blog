import pytest  # type: ignore

from app.schemas.comment_schema import CommentRequest
from app.services.comment_service import CommentService
from app.models.post_model import Post

r = 'Implementar depois'  # type:ignore
# @pytest.mark.skip(reason=r)
# INFO: OK Tests


def test_list_comments_create_ok(comment_service: CommentService, post: Post) -> None:
    new_comment = CommentRequest(content='Comentario')
    comment_db = comment_service.create(new_comment, post)

    assert comment_db
    assert comment_db.content == 'Comentario'


def test_comments_list_comments_ok(comment_service: CommentService, post: Post) -> None:
    new_comment = CommentRequest(content='Comentario')
    comment_service.create(new_comment, post)

    comment_list = comment_service.list_comments()
    assert len(comment_list) == 1
    assert comment_list[0].content == 'Comentario'


def test_comments_get_by_id_ok(comment_service: CommentService, post: Post) -> None:
    new_comment = CommentRequest(content='Comentario')
    comment_service.create(new_comment, post)

    comment_db = comment_service.get_by_id(1)
    assert comment_db
    assert comment_db.id == 1


def test_comments_update_ok(comment_service: CommentService, post: Post) -> None:
    new_comment = CommentRequest(content='Comentario')
    comment_service.create(new_comment, post)

    updated_comment = CommentRequest(content='Comentario2')
    comment_db = comment_service.update(1, updated_comment)
    assert comment_db
    assert comment_db.content == 'Comentario2'


def test_comments_delete_ok(comment_service: CommentService, post: Post) -> None:
    new_comment = CommentRequest(content='Comentario')
    new_comment_db = comment_service.create(new_comment, post)

    assert new_comment_db.id
    comment_service.delete(new_comment_db.id)
    assert comment_service.list_comments() == []
