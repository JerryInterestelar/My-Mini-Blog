from sqlmodel import Session, select

from app.core.exceptions import UserNotFoundError, EmailAlreadyExistsError
from app.core.security import get_password_hash
from app.schemas.user_scheme import UserRequest
from app.models.user_model import User


class UserService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def create(self, user: UserRequest) -> User:
        user_exists: User | None = self.session.exec(
            select(User).where(User.email == user.email)
        ).one_or_none()
        if user_exists:
            raise EmailAlreadyExistsError('Este email já está sendo usado')
        user_db: User = User.model_validate(user)
        user_db.password = get_password_hash(user.password)
        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)
        return user_db

    def list_users(self) -> list[User]:
        users_db: list[User] = list(self.session.exec(select(User)).all())
        return users_db

    def get_by_id(self, id: int) -> User:
        user_db: User | None = self.session.get(User, id)
        if user_db is None:
            raise UserNotFoundError('Usuário não encontrado')
        return user_db

    def get_by_email(self, email: str) -> User:
        user_db: User | None = self.session.exec(
            select(User).where(User.email == email)
        ).one_or_none()
        if user_db is None:
            raise UserNotFoundError('Usuário não encontrado')
        return user_db

    def update(self, user_id: int, updated_user: UserRequest) -> User:
        # Aqui fica a verificação quando tiver passando o current_user
        user_db: User | None = self.get_by_id(user_id)
        if not user_db:
            raise UserNotFoundError('Usuário não encontrado')
        user_db.name = updated_user.name
        user_db.email = updated_user.email
        user_db.password = get_password_hash(updated_user.password)

        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)
        return user_db

    def delete(self, user_id: int) -> None:
        # Aqui fica a verificação quando tiver passando o current_user
        user_db: User | None = self.get_by_id(user_id)
        self.session.delete(user_db)
        self.session.commit()
