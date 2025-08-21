import json
import hashlib
import base64

from app.cache import redis


class ResumeCache:
    TTL = 6 * 60 * 60  # 6 hours

    @staticmethod
    def _hash(file_bytes):
        return hashlib.md5(file_bytes).hexdigest()

    @classmethod
    async def save(cls, file_bytes: bytes):
        key = f"resume:{cls._hash(file_bytes)}"
        file_b64 = base64.b64encode(file_bytes).decode()
        await redis.hset(key, mapping={"file": file_b64})
        await redis.expire(key, cls.TTL)
        return key

    @classmethod
    async def get(cls, file_bytes: bytes):
        key = f"resume:{cls._hash(file_bytes)}"
        data = await redis.hgetall(key)
        if not data:
            return None
        file_bytes = base64.b64decode(data.get("file"))
        return file_bytes
