from src.job_recommender.api.naukri import get_naukri_job_recommendations
from src.job_recommender.api.linkedin import get_linkedin_job_recommendations
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("job-recommender")

@mcp.tool()
async def fetch_linkedin(listofkeywords:str):
    """
    Fetch job details from LinkedIn based on the provided keywords.
    """
    if not isinstance(listofkeywords, str):
        raise ValueError("listofkeywords must be a string.")
    return await get_linkedin_job_recommendations(search_query=listofkeywords,location="India")

 

@mcp.tool()
async def fetch_naukri(listofkeywords:str):
    """
    Fetch job details from Naukri based on the provided keywords.
    """
    if not isinstance(listofkeywords, str):
        raise ValueError("listofkeywords must be a string.")
    return await get_naukri_job_recommendations(search_query=listofkeywords,location="India")


if __name__ == "__main__":
    mcp.run(transport='stdio')