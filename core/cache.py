from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import json
from core.config import settings

async def setup_cache():
    print("🚀 Cache setup started...")
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="controlx-cache")
    print("✅ Cache setup complete!")

async def get_cache(key: str):
    backend = FastAPICache.get_backend()
    value = await backend.get(key)
    return json.loads(value) if value else None

async def set_cache(key: str, value: any, expire: int = 60):
    backend = FastAPICache.get_backend()
    await backend.set(key, json.dumps(value), expire=expire)