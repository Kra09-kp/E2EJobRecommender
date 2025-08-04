from src.job_recommender.api import apify_client

async def get_linkedin_job_recommendations(search_query: str, location: str, rows: int = 100):
    url = f"https://www.linkedin.com/jobs/search?keywords={search_query[:2]}&location={location}"
    
    run_input = {
        "urls": [url],
        "scrapeCompany": True,
        "count": rows,
    }

    try:
        actor_client = apify_client.actor("hKByXkMQaC5Qt9UMN")
        call_result = await actor_client.call(run_input=run_input)

        if not call_result or "defaultDatasetId" not in call_result:
            print("❌ No dataset ID found in call result.")
            return None

        dataset_id = call_result["defaultDatasetId"]
        dataset_client = apify_client.dataset(dataset_id)
        
        items = [item async for item in dataset_client.iterate_items()]
        
        # Debug (can be removed later)
        print(f"✅ Retrieved {len(items)} items from dataset: {dataset_id}")
        
        return items

    except Exception as e:
        print(f"🔥 Error fetching LinkedIn jobs: {e}")
        return e
