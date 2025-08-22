import json
import hashlib
from jobRecommender import logger


class KeywordsCache:
    def __init__(self,session_manager):
        self.TTL = 1 * 60 * 60
        self.session_manager = session_manager

    @staticmethod
    def _hash(file_bytes):
        """
        Generates a deterministic MD5 hash for session:{session_id} & a given file bytes.
        Args:
            file_bytes (bytes): The bytes of the file to hash.
        Returns:
            str: The MD5 hash of the file bytes.
        """
        return hashlib.md5(file_bytes).hexdigest()

    async def save(self, session_id: str, file_bytes: bytes, keywords: list):
        """
        Save the keywords to Redis with TTL.
        Args:
            file_bytes (bytes): The bytes of the file to hash.
            keywords (list): The keywords data to cache.
        """
        key = f"keywords:{self._hash(file_bytes)}"
        await self.session_manager.set(session_id,key, json.dumps(keywords))
        logger.info(f"Keywords saved to cache for session:{session_id} & file hash: {self._hash(file_bytes)[:10]}...")

    async def get(self, session_id: str, file_bytes: bytes):
        """ 
        Retrieve the keywords from Redis, or None if not found.
        Args:
            file_bytes (bytes): The bytes of the file to hash.
        Returns:
            list or None: The cached keywords data, or None if not found.   
        """
        key = f"keywords:{self._hash(file_bytes)}"
        data = await self.session_manager.get(session_id,key)
        if not data:
            logger.info(f"No cached keywords found for session:{session_id} & file hash: {self._hash(file_bytes)[:10]}...")
            return None
        
        logger.info(f"Cached keywords retrieved for session:{session_id} & file hash: {self._hash(file_bytes)[:10]}...")
        # Return the parsed JSON data
        return json.loads(data) 