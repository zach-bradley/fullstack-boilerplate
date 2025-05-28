import json
import jwt
import uuid
from datetime import datetime, timedelta,timezone
from passlib.context import CryptContext
from .config import settings
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional
from .models.users import User

# Configure JWT settings
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
REFRESH_TOKEN_EXPIRE_DAYS = 7
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setup bearer token authentication
security = HTTPBearer()

def verify_password(plain_password, hashed_password):
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    """Generate an access token."""
    expire = datetime.now().astimezone(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm="HS256")

def create_refresh_token(user_id: str) -> str:
    """Generate a refresh token."""
    expire = datetime.now().astimezone(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    token = jwt.encode({"sub": user_id, "exp": expire}, settings.JWT_SECRET_KEY, algorithm="HS256")
    return token

def revoke_refresh_token(token: str, redis_client):
    """Revoke a refresh token by storing it in Redis."""
    expire_at = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    redis_client.setex(f"revoked_token:{token}", int(expire_at.total_seconds()), "revoked")

def is_refresh_token_revoked(token: str, redis_client) -> bool:
    """Check if a refresh token is revoked."""
    return redis_client.exists(f"revoked_token:{token}") > 0

def decode_token(token: str):
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_jwt_token(token: str, db: Session, redis_client) -> Optional[User]:
    """Verify the JWT token, check the cache, and retrieve the user."""
    try:
        if token.startswith("Bearer "):
            token = token.split("Bearer ")[1]  # Remove "Bearer " prefix
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token is invalid or expired")
        
        # Check the cache for the user
        cached_user_id = get_user_cache(redis_client, user_id)
        if cached_user_id:
            # If user is found in cache, return the cached user
            return cached_user_id
        
        # Cache the user data for future requests
        set_user_cache(redis_client, user_id)
        
        return cached_user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token is invalid or expired")

def serialize_user(user: User) -> dict:
    """Convert the user object into a dictionary."""
    return {
        "id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

def set_user_cache(redis_client, user_id: str):
    """Store the serialized user data in Redis."""
    redis_client.setex("user_id", 3600, json.dumps({"user_id":user_id}))  # Cache for 1 hour

def get_user_cache(redis_client, user_id: str) -> Optional[str]:
    """Retrieve the user from the Redis cache and deserialize it."""
    cached_user = redis_client.get("user_id")
    if cached_user:
        user_id = json.loads(cached_user).get("user_id", None)
        return user_id
    return None


def refresh_access_token(refresh_token):
    """Handle refreshing access and refresh tokens while checking revocation."""
    from .resolvers.types import TokenResponse
    if is_refresh_token_revoked(refresh_token):
        raise Exception("Refresh token has been revoked")

    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise Exception("Invalid refresh token")
        
        # Revoke old refresh token
        revoke_refresh_token(refresh_token)

        # Generate new access and refresh tokens
        new_access_token = create_access_token({"sub": user_id})
        new_refresh_token = create_refresh_token(user_id)

        return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)
    
    except jwt.ExpiredSignatureError:
        raise Exception("Refresh token expired")
    except jwt.PyJWTError:
        raise Exception("Invalid refresh token")