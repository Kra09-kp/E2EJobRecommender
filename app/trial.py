from cache.jobs_cache import JobCache

async def test_job_cache():
    job_cache = JobCache()

    url = "https://api.jobs.com/search?keywords=python&location=india"
    fake_response = {"jobs": ["Python Dev", "ML Engineer"]}

    # Save in Redis
    await job_cache.save(url, fake_response)
    print("✅ Saved response to cache")

    # Fetch back from Redis
    cached = await job_cache.get(url)
    print("📦 Cached response:", cached)


import asyncio

if __name__=="__main__":
    asyncio.run(test_job_cache())