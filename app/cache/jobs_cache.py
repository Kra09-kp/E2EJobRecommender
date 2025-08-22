import json
import hashlib
from jobRecommender import logger


class JobCache:
    """
    Caches job API responses based on their URLs in Redis.
    TTL: 6 hours
    """

    def __init__(self,session_manager):

        self.TTL = 1 * 60 * 60
        self.session_manager = session_manager

    @staticmethod
    def _hash(url: str):
        """Generates a deterministic MD5 hash for a given URL.
        Args:
            url (str): The URL to hash."""
        return hashlib.md5(url.encode()).hexdigest()

    async def save(self, session_id: str, url: str, response: list[dict]):
        """Save the job response to Redis with TTL.
        Args:
            url (str): The URL of the job.
            response (dict): The job response data to cache.
        """
        key = f"jobs:{self._hash(url)}"
        await self.session_manager.set(session_id, key, json.dumps(response))
        logger.info(f"Job response cached for session:{session_id} &  URL: {url}")

    async def get(self, session_id: str, url: str):
        """Retrieve the job response from Redis, or None if not found.
        Args:
            url (str): The URL of the job.
        Returns:
            dict or None: The cached job response data, or None if not found.
        """
        key = f"jobs:{self._hash(url)}"
        data = await self.session_manager.get(session_id,key)
        if not data:
            logger.info(f"No cached job response found for session:{session_id} & URL: {url}")
            return None
        logger.info(f"Cached job response retrieved for session:{session_id} & URL: {url}")
        return json.loads(data) 
