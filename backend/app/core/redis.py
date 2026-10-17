"""Redis client configuration"""

import redis.asyncio as redis
from app.core.config import get_settings

settings = get_settings()

# Create Redis connection pool
redis_pool = redis.ConnectionPool.from_url(
    settings.REDIS_URL,
    max_connections=settings.REDIS_POOL_SIZE,
    decode_responses=True,
)


async def get_redis() -> redis.Redis:
    """Dependency for getting Redis client"""
    return redis.Redis(connection_pool=redis_pool)


async def init_redis():
    """Initialize Redis connection"""
    client = redis.Redis(connection_pool=redis_pool)
    await client.ping()
    await client.close()


async def close_redis():
    """Close Redis connections"""
    await redis_pool.disconnect()
