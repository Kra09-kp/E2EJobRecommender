import json
import hashlib
from jobRecommender import logger



class SuggestionsCache:
    def __init__(self,session_manager):
        self.TTL = 1 * 60 * 60
        self.session_manager = session_manager

    @staticmethod
    def _hash(file_bytes: bytes):
        """Generates a deterministic MD5 hash for session:{session_id} & a given file bytes.
        Args:
            file_bytes (bytes): The bytes of the file to hash.
        Returns:
            str: The MD5 hash of the file bytes.
        """
        return hashlib.md5(file_bytes).hexdigest()

    async def save(self, session_id: str, file_bytes: bytes, suggestions: dict):
        """Save the suggestions to Redis with TTL.
        Args:
            file_bytes (bytes): The bytes of the file to hash.
            suggestions (dict): The suggestions data to cache.
        """
        
        key = f"suggestions:{self._hash(file_bytes)}"
        await self.session_manager.set(session_id,key, json.dumps(suggestions))

    async def get(self, session_id: str, file_bytes: bytes):
        """Retrieve the suggestions from Redis, or None if not found.
        Args:
            file_bytes (bytes): The bytes of the file to hash.
        Returns:    
            dict or None: The cached suggestions data, or None if not found.
        """
        key = f"suggestions:{self._hash(file_bytes)}"
        data = await self.session_manager.get(session_id,key)
        if not data:
            logger.info(f"No cached suggestions found for session:{session_id} & file hash: {self._hash(file_bytes)[:10]}...")
            return None
        logger.info(f"Cached suggestions retrieved for session:{session_id} & file hash: {self._hash(file_bytes)[:10]}...")
        # Return the parsed JSON data
        return json.loads(data)