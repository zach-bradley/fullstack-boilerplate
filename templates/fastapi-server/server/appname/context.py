import strawberry
from uuid import UUID
from sqlalchemy.orm import Session
from typing import Optional
from redis import Redis
from fastapi import Request,Depends
from .database import get_db
from .models.users import UserManager, User
from .auth import verify_jwt_token
from .redis import get_redis

class MyContext(strawberry.fastapi.BaseContext):
    def __init__(self, db: Session, redis_client: Redis, user_id: Optional[str] = None):
        self.db = db
        self.redis_client = redis_client
        self.user_id = user_id

    def invalidate_user_cache(self, user_email: str):
        """Invalidate cache related to the user."""
        self.redis_client.delete(f"user:{user_email}")

    def get_user_id(self, request: Request) -> Optional[str]:
        """Authenticate and retrieve the user id from Redis or the database."""
        token = request.headers.get("Authorization")
        if not token:
            return None  # Return None if no token is provided

        user_id = verify_jwt_token(token, self.db, self.redis_client)
        return user_id
    
    def get_current_user(self) -> User:
        user_manager = UserManager(self.db)
        user = user_manager.get_by_id(self.user_id)
        return user

async def get_context(request: Request, db: Session = Depends(get_db), redis_client = Depends(get_redis)) -> MyContext:
    # Retrieve the current user using the context method
    if "/graphql" in str(request.url) and not request.headers.get("Authorization"):
        return MyContext(db=db, redis_client=redis_client,user_id=None)
    user_id = MyContext(db, redis_client).get_user_id(request)
    return MyContext(db=db, redis_client=redis_client, user_id=user_id)