import json
import hashlib
import base64

from app.cache import redis



class SuggestionsCache:
    TTL = 6 * 60 * 60

    @staticmethod
    def _hash(file_bytes: bytes):
        return hashlib.md5(file_bytes).hexdigest()

    @classmethod
    async def save(cls, file_bytes: bytes, suggestions: dict):
        key = f"suggestions:{cls._hash(file_bytes)}"
        await redis.set(key, json.dumps(suggestions), ex=cls.TTL)

    @classmethod
    async def get(cls, file_bytes: bytes):
        key = f"suggestions:{cls._hash(file_bytes)}"
        data = await redis.get(key)
        return json.loads(data) if data else None
