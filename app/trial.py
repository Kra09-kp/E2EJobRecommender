from cache.jobs_cache import JobCache
from cache.suggestions_cache import SuggestionsCache
from cache.keywords_cache import KeywordsCache
from cache.resume_cache import ResumeCache
from services.session_manager import SessionManager
from services.redis_config import RedisConfig

session_manager = None
session_id = ''


async def init_session_manager():
    
    redis_config = RedisConfig()
    client = await redis_config.init()
    session_manager = SessionManager(client)

    id = session_manager.create_session_id()
    return session_manager,id


async def test_job_cache():
    job_cache = JobCache(session_manager)

    urls =[ "https://api.jobs.com/linkedin/search?keywords=python&location=india",
    "https://api.jobs.com/naukri/search?keywords=python&location=india"]
    fake_responses = [{"jobs": ["Python Dev", "ML Engineer"]},
                      {"jobs": ["Data Scientist", "MLOPS Engineer"]}]

    for url , fake_response in zip(urls,fake_responses):
        # check if the data already save if yes then just load
        cached = await job_cache.get(session_id,url)
        if cached:
            print("📦 Already Cached response:", cached)
            return
        print("🔍 No cache found, saving response...",cached)
        # Save in Redis
        await job_cache.save(session_id,url, fake_response)
        print("✅ Saved response to cache")

        # Fetch back from Redis
        cached = await job_cache.get(session_id,url)
        print("📦 Cached response:", cached)

async def test_suggestions_cache():
    suggestions_cache = SuggestionsCache(session_manager)

    file_bytes = b"example file content"
    suggestions = {"suggestion1": "Improve resume", "suggestion2": "Add skills"}

    # check if the data already save if yes then just load
    cached_suggestions = await suggestions_cache.get(session_id,file_bytes)
    if cached_suggestions:
        print("📦 Already Cached suggestions:", cached_suggestions)
        return
    print("🔍 No cache found, saving suggestions...",cached_suggestions)
    # Save in Redis
    await suggestions_cache.save(session_id,file_bytes, suggestions)
    print("✅ Saved suggestions to cache")

    # Fetch back from Redis
    cached_suggestions = await suggestions_cache.get(session_id,file_bytes)
    print("📦 Cached suggestions:", cached_suggestions)

async def test_keywords_cache():
    keywords_cache = KeywordsCache(session_manager)

    file_bytes = b"example file content"
    keywords = ["python", "developer", "machine learning"]

    # check if the data already save if yes then just load
    cached_keywords = await keywords_cache.get(session_id,file_bytes)
    if cached_keywords:
        print("📦 Already Cached keywords:", cached_keywords)
        return
    print("🔍 No cache found, saving keywords...",cached_keywords)
    # Save in Redis
    await keywords_cache.save(session_id,file_bytes, keywords)
    print("✅ Saved keywords to cache")

    # Fetch back from Redis
    cached_keywords = await keywords_cache.get(session_id,file_bytes)
    print("📦 Cached keywords:", cached_keywords)

async def test_resume_cache():
    resume_cache = ResumeCache(session_manager)

    file_name = b"resume.pdf"
    with open("sample_resume.txt","r") as f:
        data = f.read()

    file_bytes = data.encode()

    # check if the data already save if yes then just load
    cached_resume = await resume_cache.get(session_id,file_name)
    if cached_resume:
        print(type(cached_resume))
        print("📦 Already Cached resume:", cached_resume.decode())
        return
    print("🔍 No cache found, saving resume...",cached_resume)
    # Save in Redis
    await resume_cache.save(session_id,file_name, file_bytes)
    print("✅ Saved resume to cache")

    # Fetch back from Redis
    cached_resume = await resume_cache.get(session_id,file_name)
    
    print("📦 Cached resume:", cached_resume.decode()) # type:ignore


import asyncio

async def main():
    global session_manager
    global session_id
    if session_manager is None:
        session_manager,session_id = await init_session_manager()
    else:
        session_id = session_manager.create_session_id()
    print(f"Session ID: {session_id}")
    await test_job_cache()
    await test_suggestions_cache()
    await test_keywords_cache()
    await test_resume_cache()
    print("You did it !")


if __name__=="__main__":
    asyncio.run(main())