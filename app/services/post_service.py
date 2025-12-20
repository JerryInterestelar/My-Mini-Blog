from datetime import datetime, timezone
from sqlmodel import Session, select

from app.core.exceptions import PostNotFoundError, UserHasNoPermissionsError
from app.models.user_model import User
from app.models.post_model import Post
from app.schemas.post_schema import PostRequest


class PostService:
    def __init__(self, current_user: User, session: Session) -> None:
        self.current_user = current_user
        self.session = session

    def create(self, new_post: PostRequest) -> Post:
        post_db = Post.model_validate(new_post)
        post_db.user_id = self.current_user.id
        self.session.add(post_db)
        self.session.commit()
        self.session.refresh(post_db)
        return post_db

    def list_posts(self) -> list[Post]:
        return list(self.session.exec(select(Post)).all())

    def get_by_id(self, post_id: int) -> Post:
        post_db: Post | None = self.session.get(Post, post_id)
        if post_db is None:
            raise PostNotFoundError('Postagem não encontrada')
        return post_db

    def update(self, post_id: int, updated_post: PostRequest) -> Post:
        post_db: Post = self.get_by_id(post_id)

        if post_db.user_id != self.current_user.id:
            raise UserHasNoPermissionsError(
                'Este usuário não tem permissão para alterar este post'
            )
        post_db.title = updated_post.title
        post_db.content = updated_post.content
        post_db.updated_at = datetime.now(timezone.utc)
        self.session.add(post_db)
        self.session.commit()
        self.session.refresh(post_db)
        return post_db

    def delete(self, post_id: int) -> None:
        post_db: Post = self.get_by_id(post_id)

        if post_db.user_id != self.current_user.id:
            raise UserHasNoPermissionsError(
                'Este usuário não tem permissão para alterar este post'
            )
        self.session.delete(post_db)
        self.session.commit()
