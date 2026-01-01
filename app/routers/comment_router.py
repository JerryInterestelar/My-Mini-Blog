from fastapi import APIRouter, status, HTTPException

from app.core.exceptions import CommentNotFoundError, UserHasNoPermissionsError
from app.models.comment_model import Comment
from app.schemas.comment_schema import CommentRequest, CommentResponse
from app.core.dependecies import comment_service_dep


router = APIRouter(prefix='/comments', tags=['Comments'])


@router.put(
    '/{comment_id}', status_code=status.HTTP_200_OK, response_model=CommentResponse
)
def update_comment(
    comment_id: int,
    comment_service: comment_service_dep,
    updated_comment: CommentRequest,
) -> Comment:
    try:
        return comment_service.update(comment_id, updated_comment)
    except CommentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserHasNoPermissionsError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete(
    '/{comment_id}', status_code=status.HTTP_200_OK, response_model=dict[str, str]
)
def delete_comment(
    comment_id: int,
    comment_service: comment_service_dep,
) -> dict[str, str]:
    try:
        comment_service.delete(comment_id)
        return {'message': f'Comentário de id: {comment_id} deletado com sucesso'}
    except CommentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserHasNoPermissionsError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
