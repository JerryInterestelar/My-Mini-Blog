from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import PostNotFoundError, UserHasNoPermissionsError
from app.models.comment_model import Comment
from app.models.post_model import Post
from app.schemas.comment_schema import CommentRequest, CommentResponse
from app.schemas.post_schema import PostRequest, PostResponse
from app.core.dependecies import post_user_service_dep, post_public_service_dep
from app.services.comment_service import CommentService

router = APIRouter(prefix='/posts', tags=['Posts'])

# INFO: Gerenciamento de Postagens


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostRequest, post_user_service: post_user_service_dep) -> Post:
    return post_user_service.create(post)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[PostResponse])
def get_posts(post_public_service: post_public_service_dep) -> list[Post]:
    return post_public_service.list_posts()


@router.get('/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post(post_id: int, post_public_service: post_public_service_dep) -> Post:
    try:
        return post_public_service.get_by_id(post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put('/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(
    post_id: int, updated_post: PostRequest, post_user_service: post_user_service_dep
) -> Post:
    try:
        return post_user_service.update(post_id, updated_post)
    except PostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserHasNoPermissionsError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete(
    '/{post_id}', status_code=status.HTTP_200_OK, response_model=dict[str, str]
)
def delete_post(
    post_id: int, post_user_service: post_user_service_dep
) -> dict[str, str]:
    try:
        post_user_service.delete(post_id)
        return {'message': f'Postagem de id: {post_id} deletada com sucesso'}
    except PostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserHasNoPermissionsError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


# INFO: Gerenciamento de Comentários
# TODO: Com a refatoração de CommentService, ver ser dá pra implementar ele aqui melhor
@router.post(
    '/{post_id}/comments',
    status_code=status.HTTP_201_CREATED,
    response_model=CommentResponse,
)
def create_comment(
    post_id: int, post_user_service: post_user_service_dep, new_comment: CommentRequest
) -> Comment:
    try:
        current_post = post_user_service.get_by_id(post_id)
        comment_service = CommentService(
            post_user_service.session, post_user_service.current_user
        )
        return comment_service.create(new_comment, current_post)
    except PostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    '/{post_id}/comments',
    status_code=status.HTTP_200_OK,
    response_model=list[CommentResponse],
)
def list_post_comments(
    post_id: int, post_user_service: post_user_service_dep
) -> list[Comment]:
    try:
        return post_user_service.get_by_id(post_id).comments
    except PostNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
