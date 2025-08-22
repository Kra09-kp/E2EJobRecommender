import json
import hashlib
import base64
from jobRecommender import logger


class ResumeCache:
    def __init__(self,session_manager): 
        self.TTL = 1 * 60 * 60
        self.session_manager = session_manager

    @staticmethod
    def _hash(file_bytes):
        return hashlib.md5(file_bytes).hexdigest()

    async def save(self, session_id: str,file_name:bytes, file_bytes: bytes):
        """ Save the resume file to Redis with TTL.
        Args:
            file_name (bytes): The name of the file to hash.(Key)
            file_bytes (bytes): The bytes of the resume file to cache. (Value)
        """
        key = f"resume:{self._hash(file_name)}"
        file_b64 = base64.b64encode(file_bytes).decode()
        await self.session_manager.set(session_id,key, json.dumps({"file": file_b64 }))
        logger.info(f"Resume saved to cache for session:{session_id} & file hash: {self._hash(file_name)[:10]}...")

    async def get(self, session_id: str, file_name: bytes):
        key = f"resume:{self._hash(file_name)}"
        data = await self.session_manager.get(session_id,key)
        if not data:
            logger.info(f"No cached resume found for session:{session_id} & file hash: {self._hash(file_name)[:10]}...")
            return None
        data = json.loads(data)
        # print("Data",data)
        file_bytes = base64.b64decode(data["file"])
        # print("after decoding",file_bytes)
        logger.info(f"Cached resume retrieved for session:{session_id} & file hash: {self._hash(file_name)[:10]}...")
        # Return the bytes of the file
        return file_bytes
