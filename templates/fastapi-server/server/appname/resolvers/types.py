import strawberry
import typing

# Types
@strawberry.type
class TokenResponse:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@strawberry.type
class UserType:
    id: strawberry.ID
    email: str
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None    

# Inputs
@strawberry.input
class UserInput:
    email: str
    password: str
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None

@strawberry.input
class UserLoginInput:
    email: str
    password: str

@strawberry.input
class UserUpdateInput:
    id: strawberry.ID
    first_name: typing.Optional[str] = None
    last_name: typing.Optional[str] = None
    email: typing.Optional[str] = None   