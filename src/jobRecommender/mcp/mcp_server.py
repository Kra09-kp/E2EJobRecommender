from jobRecommender.api.naukri import get_naukri_job_recommendations
from jobRecommender.api.linkedin import get_linkedin_job_recommendations
from mcp.server.fastmcp import FastMCP
from jobRecommender import logger

mcp = FastMCP("job-recommender")

@mcp.tool()
async def fetch_linkedin(listofkeywords:list[str]):
    """
    Fetch job details from LinkedIn based on the provided keywords.
    """
    logger.info(f"Fetching LinkedIn jobs for keywords: {listofkeywords}")
    if not isinstance(listofkeywords, list):
        logger.error("listofkeywords must be a list of strings.")
        raise ValueError("listofkeywords must be a list of strings.")

    for keyword in listofkeywords:
        if not isinstance(keyword, str):
            logger.error("Each keyword must be a string.")
            raise ValueError("Each keyword must be a string.")

    return await get_linkedin_job_recommendations(search_query=listofkeywords,location="India")

 

@mcp.tool()
async def fetch_naukri(listofkeywords:list[str]):
    """
    Fetch job details from Naukri based on the provided keywords.
    """
    logger.info(f"Fetching Naukri jobs for keywords: {listofkeywords}")
    if not isinstance(listofkeywords, list):
        logger.error("listofkeywords must be a list of strings.")
        raise ValueError("listofkeywords must be a list of strings.")
    for keyword in listofkeywords:
        if not isinstance(keyword, str):
            logger.error("Each keyword must be a string.")
            raise ValueError("Each keyword must be a string.")

    return await get_naukri_job_recommendations(search_query=listofkeywords,location="India")


if __name__ == "__main__":
    mcp.run(transport='stdio')