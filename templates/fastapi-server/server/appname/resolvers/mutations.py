
import strawberry
from typing import Optional
from uuid import UUID
from .user_resolvers import UserResolvers
from .types import UserType, UserInput, TokenResponse, UserUpdateInput

@strawberry.type
class UserMutation:
    @strawberry.mutation
    def register(self, userData: UserInput, info: strawberry.Info) -> UserType:
        db = info.context.db
        return UserResolvers.create_user(userData, db)
    
    @strawberry.mutation
    def update_user(self, userData: UserUpdateInput,info:strawberry.Info) -> UserType:
        db = info.context.db
        return UserResolvers.update_user(userData,db)
    
    @strawberry.mutation
    def login(self, email: str, password: str, info: strawberry.Info) -> TokenResponse:
        db = info.context.db
        return UserResolvers.login(email, password, db)
    
    @strawberry.mutation
    def reset_password(self,email: str,new_password:str,info:strawberry.Info) -> bool:
        db = info.context.db
        return UserResolvers.reset_password(email,new_password, db)
    
    @strawberry.mutation
    def logout(self, refresh_token:str,info: strawberry.Info) -> bool:
        from ..auth import revoke_refresh_token
        user = info.context.get_current_user()

        info.context.invalidate_user_cache(user.email)
        revoke_refresh_token(refresh_token, info.context.redis_client)
        return True