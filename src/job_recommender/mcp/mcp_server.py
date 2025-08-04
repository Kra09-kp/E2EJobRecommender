from src.job_recommender.api.naukri import get_naukri_job_recommendations
from src.job_recommender.api.linkedin import get_linkedin_job_recommendations
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("job-recommender")

@mcp.tool()
async def fetch_linkedin(listofkeywords):
    """
    Fetch job details from LinkedIn based on the provided keywords.
    """
    return await get_linkedin_job_recommendations(search_query=listofkeywords,location="India")

 

@mcp.tool()
async def fetch_naukri(listofkeywords):
    """
    Fetch job details from Naukri based on the provided keywords.
    """
    return await get_naukri_job_recommendations(search_query=listofkeywords,location="India")


def start():
    """
    Starts the MCP server.
    """
    mcp.run(transport='stdio')


if __name__ == "__main__":
    start()