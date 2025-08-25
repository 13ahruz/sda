from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from ..core.config import settings

async def init_cache():
    redis = aioredis.from_url(settings.get_redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="sda_cache:")
