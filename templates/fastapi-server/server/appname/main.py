import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from strawberry.fastapi import GraphQLRouter
from .redis import get_redis,shutdown_redis
from redis.exceptions import ConnectionError
from .routers.graphql import schema
from .database import engine, Base
from .context import get_context

Base.metadata.create_all(bind=engine)

async def wait_for_redis():
    redis_client = get_redis()
    retry_count = 5
    while retry_count > 0:
        try:
            # Ping Redis to check if it's responsive
            if redis_client.ping():
                print("Redis is available!")
                return
        except ConnectionError:
            retry_count -= 1
            print(f"Redis not available yet, retrying... ({retry_count} attempts left)")
            await asyncio.sleep(2)  # Wait for 2 seconds before retrying
    raise Exception("Could not connect to Redis after multiple attempts")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting app...")
    await wait_for_redis()
    yield
    print("Shutting down!")


app = FastAPI(lifespan=lifespan)
graphql_app = GraphQLRouter(schema,context_getter=get_context,graphql_ide=True)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with GraphQL!"}
