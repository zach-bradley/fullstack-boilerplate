import strawberry
from ..resolvers.queries import Query
from ..resolvers.mutations import UserMutation

@strawberry.type
class Mutation(UserMutation):
    pass

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)