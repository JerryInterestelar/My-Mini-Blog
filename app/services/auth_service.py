from sqlmodel import Session

from app.core.security import verify_password_hash, create_access_token
from app.models.user_model import User
from app.schemas.token_schema import Token
from app.core.exceptions import UserEmailOrPassIncorrectError, UserNotFoundError
from app.services.user_service import UserService


class AuthService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.service: UserService = UserService(self.session)

    # IMPLEMENT: Adicionar verificação de usuário ativo (ex: if user.disabled: raise Error).
    def authenticate(self, email: str, password: str) -> Token:
        try:
            user_db: User = self.service.get_by_email(email)

            if not verify_password_hash(password, user_db.password):
                raise UserEmailOrPassIncorrectError('Email ou Senha Incorretos')
        except UserNotFoundError:
            raise UserEmailOrPassIncorrectError('Email ou Senha Incorretos')

        access_token: str = create_access_token(data={'sub': user_db.email})
        return Token(access_token=access_token, token_type='bearer')
