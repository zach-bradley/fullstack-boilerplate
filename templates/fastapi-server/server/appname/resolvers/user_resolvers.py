
from typing import Optional, List as PyList
from uuid import UUID
from sqlalchemy.orm import Session
from ..models.users import UserManager
from .types import UserType, UserInput, TokenResponse, UserUpdateInput
from..schemas.user_schemas import UserUpdate
from ..auth import create_access_token, create_refresh_token
from datetime import timedelta

class UserResolvers:
    @staticmethod
    def get_user(id: UUID, db: Session) -> Optional[UserType]:
        user_manager = UserManager(db)
        user = user_manager.get_by_id(id)
        return UserType(**user.client_dict()) if user else None

    @staticmethod
    def get_users(db: Session) -> PyList[UserType]:
        user_manager = UserManager(db)
        users = user_manager.get_all()
        return [UserType(**user.client_dict()) for user in users]

    @staticmethod
    def create_user(userData: UserInput, db: Session) -> UserType:
        user_manager = UserManager(db)
        user_dict = userData.__dict__.copy()
        db_user = user_manager.create_user(user_dict)
        return db_user
    
    @staticmethod
    def update_user(user_data: UserUpdateInput, db: Session) -> UserType:
        user_manager = UserManager(db)
        validated_data = UserUpdate(**user_data.__dict__.copy())
        db_user = user_manager.update(user_data.id, validated_data)
        return user_manager.serialize_user(db_user)
    
    @staticmethod
    def login(email: str, password: str, db: Session) -> TokenResponse:
        user_manager = UserManager(db)
        user = user_manager.get_user_by_email(email)
        if not user or not user_manager.verify_password(password, user.password):

            raise ValueError("Incorrect email or password")
        
        access_token = create_access_token(
            data={"sub": str(user.id)}
        )
        refresh_token = create_refresh_token(str(user.id))
        
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    
    @staticmethod
    def reset_password(email: str, new_password: str, db: Session) -> bool:
        try:
            user_manager = UserManager(db)
            user = user_manager.get_user_by_email(email)
            
            if not user:
                raise ValueError("User not found")

            success = user_manager.reset_password(user, new_password)
            
            if success:
                return True
            else:
                raise ValueError("Password reset failed")

        except Exception:
            return False
        
    @staticmethod
    def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Handle refreshing access and refresh tokens while checking revocation."""
        from ..auth import refresh_access_token
        return refresh_access_token(refresh_token)