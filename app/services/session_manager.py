import uuid


class SessionManager:
    def __init__(self, redis_client, ttl: int = 43200):
        """
        :param redis_client: Redis connection (from RedisConfig)
        :param ttl: Expiration time in seconds (default 12 hours)
        """
        self.redis = redis_client
        self.ttl = ttl

    def create_session_id(self) -> str:
        """Generate unique session ID"""
        return str(uuid.uuid4())

    async def set(self, session_id: str, key: str, value: str):
        """Store session data with TTL"""
        redis_key = f"session:{session_id}:{key}"
        await self.redis.set(redis_key, value, ex=self.ttl)

    async def get(self, session_id: str, key: str):
        """Retrieve session data"""
        redis_key = f"session:{session_id}:{key}"
        return await self.redis.get(redis_key)

    async def delete(self, session_id: str):
        """Delete all keys for a session"""
        pattern = f"session:{session_id}:*"
        async for key in self.redis.scan_iter(match=pattern):
            await self.redis.delete(key)
