from redis import Redis
from .config import settings

print(settings.REDIS_HOST)
redis_client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

# Dependency function to provide access to the Redis client
def get_redis() -> Redis:
    return redis_client

# Shutdown logic to close Redis connection
async def shutdown_redis():
    redis_client.close()