from redis import asyncio as redis_asyncio

#  Initialize Redis connection (reuse for all classes)
redis_con = redis_asyncio.from_url("redis://localhost", decode_responses=True)
