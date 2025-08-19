from jobRecommender.api import apify_client
from jobRecommender import logger


async def get_naukri_job_recommendations(search_query:str,location:str,rows=70):
    """
    Fetches job listings from Naukri based on a search query and location.

    Args:
        search_query (str): The job title or keywords to search for.
        location (str): The location to search for jobs in.
        rows (int, optional): The number of job listings to fetch. Defaults to 60.

    Returns:
        list: A list of dictionaries containing job details.
    """
    # print(search_query)
    run_input = {
        "keyword": search_query,
        "maxJobs": rows,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all",
        "location": location,
    }
    try:
        actor_client = apify_client.actor("alpcnRV9YI9lYVPWk")
        call_result = await actor_client.call(run_input=run_input)

        if not call_result or "defaultDatasetId" not in call_result:
            logger.info("❌ No dataset ID found in call result.")
            return None
        
        dataset_id = call_result["defaultDatasetId"]
        dataset_client = apify_client.dataset(dataset_id)
        items = [item async for item in dataset_client.iterate_items()]
        logger.info(f"✅ Retrieved {len(items)} items from dataset: {dataset_id}")
        return items
    
    except Exception as e:
        logger.error(f"🔥 Error fetching Naukri jobs: {e}")
        return e