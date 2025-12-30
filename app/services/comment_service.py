from sqlmodel import Session, select

from app.core.exceptions import CommentNotFoundError, UserHasNoPermissionsError
from app.models.post_model import Post
from app.models.user_model import User
from app.models.comment_model import Comment
from app.schemas.comment_schema import CommentRequest


class CommentService:
    def __init__(self, session: Session, user: User) -> None:
        self.session = session
        self.user = user

    def create(self, new_comment: CommentRequest, post: Post) -> Comment:
        new_comment_db = Comment(
            **new_comment.model_dump(),
            user=self.user,
            post=post,
        )
        self.session.add(new_comment_db)
        self.session.commit()
        self.session.refresh(new_comment_db)
        return new_comment_db

    def list_comments(self) -> list[Comment]:
        return list(self.session.exec(select(Comment)).all())

    def get_by_id(self, comment_id: int) -> Comment:
        comment_db = self.session.get(Comment, comment_id)
        if comment_db is None:
            raise CommentNotFoundError('Comentário não encontrado.')
        return comment_db

    def update(self, comment_id: int, updated_comment: CommentRequest) -> Comment:
        comment_db = self.get_by_id(comment_id)
        if comment_db.user_id != self.user.id:
            raise UserHasNoPermissionsError(
                'Este usuário não tem permissão para alterar este comentário'
            )
        comment_db.content = updated_comment.content
        self.session.add(comment_db)
        self.session.commit()
        self.session.refresh(comment_db)
        return comment_db

    def delete(self, comment_id: int) -> None:
        comment_db = self.get_by_id(comment_id)
        if comment_db.user_id != self.user.id:
            raise UserHasNoPermissionsError(
                'Este usuário não tem permissão para alterar este comentário'
            )
        self.session.delete(comment_db)
        self.session.commit()
