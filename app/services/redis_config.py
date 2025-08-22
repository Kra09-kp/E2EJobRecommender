import redis.asyncio as redis_asyncio


class RedisConfig:
    def __init__(self, host="localhost", port=6379, db=0, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.client = None

    async def init(self):
        """Initialize Redis client"""
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
