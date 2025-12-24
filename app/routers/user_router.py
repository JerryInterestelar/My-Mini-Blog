from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import EmailAlreadyExistsError, UserNotFoundError
from app.models.user_model import User
from app.schemas.user_scheme import UserRequest, UserResponse
from app.core.dependecies import user_service_dep, current_user_dep

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[UserResponse])
def get_users(service: user_service_dep) -> list[User]:
    list_users: list[User] = service.list_users()
    return list_users


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(user_id: int, service: user_service_dep) -> User | None:
    try:
        user_db: User | None = service.get_by_id(user_id)
        return user_db
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserRequest, service: user_service_dep) -> User:
    try:
        user_db: User = service.create(user)
        return user_db
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.put('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_user(
    user_id: int,
    current_user: current_user_dep,
    updated_user: UserRequest,
    service: user_service_dep,
) -> User:
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='O usuário não tem permissão de alterar outro usuário',
            )
        user_db: User = service.update(user_id, updated_user)
        return user_db
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete(
    '/{user_id}', status_code=status.HTTP_200_OK, response_model=dict[str, str]
)
def delete_user(
    user_id: int, current_user: current_user_dep, service: user_service_dep
) -> dict[str, str]:
    try:
        if user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='O usuário não tem permissão de alterar outro usuário',
            )
        service.delete(user_id)
        return {'Message': f'Usuário com ID: {user_id} foi deletado com sucesso.'}
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
