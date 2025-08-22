from app.model.ask_llm import AskLLM
from jobRecommender.api.linkedin import get_linkedin_job_recommendations
from jobRecommender.api.naukri import get_naukri_job_recommendations
from jobRecommender.utils.helper import  make_data_clean
from jobRecommender import logger
from io import BytesIO
from pdfminer.high_level import extract_text
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File
# from app.main import session_manager
from app.cache.jobs_cache import JobCache
from app.cache.keywords_cache import KeywordsCache
from app.cache.resume_cache import ResumeCache

# Tell FastAPI where templates are
templates = Jinja2Templates(directory="app/templates")  


router = APIRouter()
ask_llm = AskLLM()

class ResumeRequest(BaseModel):
    resume_text: str

class Keywords(BaseModel):
    keywords: list[str]
#     



@router.post("/keywords")
async def job_recommendation(request:Request,file: UploadFile = File(...)):
    """
    Get suggestions based on uploaded resume PDF.
    """
    try:
        from app.main import session_manager
        # print(file)
        session_id = request.headers.get("X-Session-Id")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required in headers")

        keywords_cache = KeywordsCache(session_manager)
        if not file.filename.endswith(".pdf"):  # type: ignore
            logger.error("Only PDF files are allowed")
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        file_content = await file.read()
        resume_text = extract_text(BytesIO(file_content)) # Pass BytesIO to your extractor
        # resume_text = extract_text_from_pdf(file.filename)  # type: ignore
        # Create ResumeRequest object dynamically
        # print(resume_text)
       
        request_obj = ResumeRequest(resume_text=resume_text)

        # check if the data already save if yes then just load
        cached_keywords = await keywords_cache.get(session_id,resume_text[:15].encode())
        if cached_keywords:
            print("📦 Already Cached keywords:", cached_keywords)
            return JSONResponse(content={"keywords": cached_keywords})
       
        

        # Call your LLM function
        # keywords = ask_llm.get_keywords(request_obj)

        keywords = ["Software Engineer",
        "Data Scientist",
        "Machine Learning Engineer",
        "Full Stack Developer",
        "DevOps Engineer"]
        keywords = Keywords(keywords=keywords)

        logger.info("Keywords are generated successfully")
        logger.info("🔍 No cache found, saving keywords...")
        # Save in Redis
        await keywords_cache.save(session_id,resume_text[:15].encode(), keywords.keywords)
        logger.info("✅ Saved keywords to cache")
        print(keywords)
        response = JSONResponse({"keywords": keywords.keywords})
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=21600)
        return response  # type: ignore

    except Exception as e:
        logger.error(f"Error while generating keywords: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
   

from fastapi import Request

@router.get("/job-recommendation/linkedin")
async def linkedin_jobs(request: Request, keywords: str = "", location: str = ""):
    try:
        from app.main import session_manager
        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required in headers")
        print(keywords)
        print(location)
        job_cache = JobCache(session_manager)
        keywords_list = []
        if "," in keywords:
            keywords_list.extend([kw.strip() for kw in keywords.split(",")])
        else:
            keywords_list.append(keywords.strip())
        print(keywords_list)

        url = f"/job-recommendation/linkedin?keywords={keywords}&location={location}"
        cache_jobs = await job_cache.get(session_id,url)
        if cache_jobs:
            print("📦 You already searched for this url so here is the cached result")
            return templates.TemplateResponse(
                "jobs.html",
                {"request": request,
                 "jobs": cache_jobs,
                 "platform": "linkedin"}
            )
        try:
            with open("artifacts/linkedin.json","r") as f:
                jobs = f.read()

            jobs = make_data_clean(jobs,"linkedin")
            print("🔍 No cache found, saving response...")
            # Save in Redis
            await job_cache.save(session_id,url, jobs)
            print("✅ Saved response to cache")

            # # Fetch back from Redis
            # cached = await job_cache.get(session_id,url)
            # print("📦 Cached response:", cached)

        except Exception as e:
            logger.error(f"Error while cleaning job: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

        logger.info("Jobs from LinkedIn fetched successfully!")
        # request object pass karna mandatory hai
        return templates.TemplateResponse(
            "jobs.html",
            {"request": request,
              "jobs": jobs,
              "platform": "linkedin"}
        )
    except Exception as e:
        logger.error(f"Error while searching job from the linkedin: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
  

@router.get("/job-recommendation/naukri")
async def naukri_jobs(request: Request, keywords: str = "", location: str = ""):
    try:
        from app.main import session_manager
        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required in headers")
        keywords_list = []
        if "," in keywords:
            keywords_list.extend([kw.strip() for kw in keywords.split(",")])
        else:
            keywords_list.append(keywords.strip())
        print(keywords_list)

        job_cache = JobCache(session_manager)
        url = f"/job-recommendation/naukri?keywords={keywords}&location={location}"

        cache_jobs = await job_cache.get(session_id,url)

        if cache_jobs:
            print("📦 You already searched for this url so here is the cached result")
            return templates.TemplateResponse(
                "jobs.html",
                {"request": request,
                 "jobs": cache_jobs,
                 "platform": "naukri"}
            )

        # jobs = await get_naukri_job_recommendations(keywords, location)

        

        try:
            with open("artifacts/naukri.json","r") as f:
                jobs = f.read()

            jobs = make_data_clean(jobs,"naukri")
            print("🔍 No cache found, saving response...")
            # Save in Redis
            await job_cache.save(session_id,url, jobs)
            print("✅ Saved response to cache")

        
        except Exception as e:
            logger.error(f"Error while cleaning job: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

        logger.info("Jobs from naukri fetched successfully!")
        return templates.TemplateResponse(
            "jobs.html", 
            {"request": request,"jobs": jobs, "platform": "naukri"}
        )

    except Exception as e:
        logger.error(f"Error while searching job from the naukri: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

 