from app.model.ask_llm import AskLLM
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from src.job_recommender.api.linkedin import get_linkedin_job_recommendations
from src.job_recommender.api.naukri import get_naukri_job_recommendations

router = APIRouter()
ask_llm = AskLLM()

class ResumeRequest(BaseModel):
    resume_text: str

class Keywords(BaseModel):
    keywords: list[str]
    location: str

@router.post("/job-recommendation")
async def job_recommendation(request: ResumeRequest):
    """
    Get suggestions based on the resume text.
    """
    try:
        keywords = ask_llm.get_keywords(request)
        print(keywords)
        return JSONResponse(content={"keywords":keywords.keywords}) #type: ignore
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("job-recommendation/linkedin")
async def linkedin_jobs(keywords: Keywords):
    try:
        jobs = await get_linkedin_job_recommendations( keywords.keywords[0],keywords.location)

        # all_jobs = ""
        # for keyword in Keywords.keywords:
        #     jobs = await get_linkedin_job_recommendations(keyword,keywords.location)
        #     all_jobs+=jobs
        return JSONResponse(content=jobs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("job-recommendation/naukri")
async def naukri_jobs(keywords: Keywords):
    try:
        jobs = await get_naukri_job_recommendations(keywords.keywords,keywords.location)
        return JSONResponse(content=jobs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
