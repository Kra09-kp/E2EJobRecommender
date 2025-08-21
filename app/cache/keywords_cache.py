import json
import hashlib
import base64

from app.cache import redis


class KeywordsCache:
    TTL = 6 * 60 * 60

    @staticmethod
    def _hash(file_bytes):
        return hashlib.md5(file_bytes).hexdigest()

    @classmethod
    async def save(cls, file_bytes: bytes, keywords: list):
        key = f"resume:{cls._hash(file_bytes)}"
        await redis.hset(key, mapping={"keywords": json.dumps(keywords)})
        await redis.expire(key, cls.TTL)

    @classmethod
    async def get(cls, file_bytes: bytes):
        key = f"resume:{cls._hash(file_bytes)}"
        data = await redis.hget(key, "keywords")
        return json.loads(data) if data else None
