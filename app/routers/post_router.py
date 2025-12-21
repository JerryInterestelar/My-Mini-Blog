from fastapi import APIRouter, status

from app.models.post_model import Post
from app.schemas.post_schema import PostRequest, PostResponse
from app.core.dependecies import post_user_service_dep, post_public_service_dep

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostRequest, post_user_service: post_user_service_dep) -> Post:
    return post_user_service.create(post)


# TODO: Implementar os erros
@router.get('/', status_code=status.HTTP_200_OK, response_model=list[PostResponse])
def get_posts(post_public_service: post_public_service_dep) -> list[Post]:
    return post_public_service.list_posts()


@router.get('/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponse)
def get_post(post_id: int, post_public_service: post_public_service_dep) -> Post:
    return post_public_service.get_by_id(post_id)


@router.put('/{post_id}', status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(
    post_id: int, updated_post: PostRequest, post_user_service: post_user_service_dep
) -> Post:
    return post_user_service.update(post_id, updated_post)


@router.delete(
    '/{post_id}', status_code=status.HTTP_200_OK, response_model=dict[str, str]
)
def delete_post(
    post_id: int, post_user_service: post_user_service_dep
) -> dict[str, str]:
    post_user_service.delete(post_id)
    return {'message': f'Postagem de id: {post_id} deletada com sucesso'}
