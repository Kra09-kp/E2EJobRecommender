import json
import hashlib
from cache import redis_con
from jobRecommender import logger

class JobCache:
    """
    Caches job API responses based on their URLs in Redis.
    TTL: 6 hours
    """

    def __init__(self):
        self.TTL = 6 * 60 * 60

    @staticmethod
    def _hash(url: str):
        """Generates a deterministic MD5 hash for a given URL.
        Args:
            url (str): The URL to hash."""
        return hashlib.md5(url.encode()).hexdigest()

    async def save(self, url: str, response: dict):
        """Save the job response to Redis with TTL.
        Args:
            url (str): The URL of the job.
            response (dict): The job response data to cache.
        """
        key = f"jobs:{self._hash(url)}"
        await redis_con.set(key, json.dumps(response), ex=self.TTL)
        logger.info(f"Job response cached for URL: {url}")

    async def get(self, url: str):
        """Retrieve the job response from Redis, or None if not found.
        Args:
            url (str): The URL of the job.
        Returns:
            dict or None: The cached job response data, or None if not found.
        """
        key = f"jobs:{self._hash(url)}"
        data = await redis_con.get(key)
        if not data:
            logger.info(f"No cached job response found for URL: {url}")
            return None
        logger.info(f"Cached job response retrieved for URL: {url}")
        return json.loads(data) 
