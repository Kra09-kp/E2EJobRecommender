from apify_client import ApifyClientAsync
from src.job_recommender.utils.helper import load_env_variables

api_key = load_env_variables("APIFY")  # Load APIFY API key

apify_client = ApifyClientAsync(api_key)