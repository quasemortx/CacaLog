from redis.asyncio import Redis

from app.config import settings

def make_redis() -> Redis | None:
    if not settings.redis_url:
        return None
    return Redis.from_url(settings.redis_url, decode_responses=True)
