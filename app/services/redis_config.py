import redis.asyncio as redis_asyncio
import os

import os
import redis.asyncio as aioredis  # assuming you are using aioredis/redis-py



class RedisConfig:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.db = int(os.getenv("REDIS_DB", 0))
        self.password = os.getenv("REDIS_PASSWORD", None)
        self.redis_url = os.getenv("REDIS_URL",None)
        self.client = None

    async def init(self):
        """Initialize Redis client"""
        if self.redis_url:
            self.client = redis_asyncio.from_url(self.redis_url,
            decode_responses=True)
            return self.client
        self.client = redis_asyncio.from_url(
            f"redis://{self.host}:{self.port}/{self.db}",
            password=self.password,
            decode_responses=True
        )
        return self.client

    async def close(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()
