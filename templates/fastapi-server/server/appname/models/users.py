import uuid
from .util import TimeStampModel, BaseManager
from sqlalchemy import Column, String, Float,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from pydantic import ValidationError
from ..schemas.user_schemas import UserCreate, UserUpdate
from typing import Optional
from sqlalchemy.orm import relationship, Session
from ..utils import model_to_dict
from ..resolvers.types import UserType

class User(TimeStampModel):
    __tablename__ = 'users'

    first_name: Optional[str] = Column(String(30), nullable=True)
    last_name: Optional[str] = Column(String(30), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']

    def __repr__(self):
        return f"<User(email={self.email})>"
    
    def client_dict(self):
        user = model_to_dict(self,UserType)
        return user
    
class UserManager(BaseManager):
    def __init__(self, db:Session):
        super().__init__(User, db)

    def serialize_user(self, user: User) -> UserType:
        """Convert the User model to UserType"""
        return UserType(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )

    def verify_password(self, password: str, hashed_password: str) -> bool:
        from ..auth import verify_password
        return verify_password(password, hashed_password)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def reset_password(self, user: User, new_password: str) -> bool:
        from ..auth import get_password_hash
        try:
            user.password = get_password_hash(new_password)
            self.db.commit()
            self.db.refresh(user)
            return True
        except Exception:
            return False

    def update_user(self,user: User, update_data: UserUpdate, redis_client):
        """
        Update user details securely and refresh the session user.
        """
        from ..auth import set_user_cache
        if update_data.email and update_data.email != user.email:
            existing_user = self.db.query(User).filter(User.email == update_data.email).first()
            if existing_user:
                raise ValueError("Email already in use")

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        set_user_cache(redis_client, user.email, user.client_dict())
        return self.serialize_user(user)
    
    def create_user(self, user_data):
        from ..auth import get_password_hash
        user_data["password"] = get_password_hash(user_data.get("password"))
        if not user_data.get("email"):
            raise ValueError("Users must have an email address")
        try:
            validated_data = UserCreate(**user_data)
        except ValidationError as e:
            raise ValueError("Error validating info: {}".format(e))
        db_user = User(**validated_data.model_dump())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return self.serialize_user(db_user)