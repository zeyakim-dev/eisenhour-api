from domain.auth.auth_info.value_objects import HashedPassword
from domain.user.user import User
from domain.user.value_objects import Email, Username
from infra.persistence.base.mapper import Mapper
from infra.persistence.sqlalchemy.postgresql.user.user_model import UserModel


class UserMapper(Mapper[User, UserModel]):
    """User 엔터티와 UserModel 간 매핑을 수행하는 매퍼 클래스."""

    def to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            username=Username(model.username),
            email=Email(model.email),
            hashed_password=HashedPassword(model.hashed_password),
        )

    def to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            username=entity.username.value,
            email=entity.email.value,
            hashed_password=entity.hashed_password.value,
        )
