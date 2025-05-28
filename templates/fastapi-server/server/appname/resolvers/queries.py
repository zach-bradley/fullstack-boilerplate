import strawberry
from typing import Optional, List as PyList
from uuid import UUID
from .user_resolvers import UserResolvers
from .types import UserType


# User resolvers
def get_me(token: str,info:strawberry.Info) -> Optional[UserType]:
    user = info.context.get_current_user()
    return UserType(**user.client_dict())

def get_user(id: UUID, info: strawberry.Info) -> Optional[UserType]:
    db = info.context.db
    return UserResolvers.get_user(id, db)

def get_users(info: strawberry.Info) -> PyList[UserType]:
    db = info.context.db
    return UserResolvers.get_users(db)

@strawberry.type
class Query:
    me: Optional[UserType] = strawberry.field(resolver=get_me)
    user: Optional[UserType] = strawberry.field(resolver=get_user)
    users: PyList[UserType] = strawberry.field(resolver=get_users)