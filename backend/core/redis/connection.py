import redis.asyncio as redis

from core.settings import settings


async def get_redis_connection():
    if not settings.REDIS_URL:
        return None
    return redis.from_url(settings.REDIS_URL)