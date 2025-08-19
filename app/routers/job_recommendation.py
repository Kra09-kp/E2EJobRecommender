from app.model.ask_llm import AskLLM
from jobRecommender.api.linkedin import get_linkedin_job_recommendations
from jobRecommender.api.naukri import get_naukri_job_recommendations
from jobRecommender.utils.helper import  make_data_clean
from jobRecommender import logger
from io import BytesIO
from pdfminer.high_level import extract_text
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File


# Tell FastAPI where templates are
templates = Jinja2Templates(directory="app/templates")  


router = APIRouter()
ask_llm = AskLLM()

class ResumeRequest(BaseModel):
    resume_text: str

class Keywords(BaseModel):
    keywords: list[str]
    location: str



@router.post("/job-recommendation")
async def job_recommendation(file: UploadFile = File(...)):
    """
    Get suggestions based on uploaded resume PDF.
    """
    try:
        # print(file)
        if not file.filename.endswith(".pdf"):  # type: ignore
            logger.error("Only PDF files are allowed")
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        file_content = await file.read()
        resume_text = extract_text(BytesIO(file_content)) # Pass BytesIO to your extractor
        # resume_text = extract_text_from_pdf(file.filename)  # type: ignore
        # Create ResumeRequest object dynamically
        # print(resume_text)
        request_obj = ResumeRequest(resume_text=resume_text)

        # Call your LLM function
        keywords = ask_llm.get_keywords(request_obj)
        logger.info("Keywords are generated successfully")
 
        return JSONResponse(content={"keywords": keywords.keywords})  # type: ignore

    except Exception as e:
        logger.error(f"Error while generating keywords: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
   

from fastapi import Request

@router.get("/job-recommendation/linkedin")
async def linkedin_jobs(request: Request, keywords: str = "", location: str = ""):
    try:
        print(keywords)
        print(location)
        keywords_list = []
        if "," in keywords:
            keywords_list.extend([kw.strip() for kw in keywords.split(",")])
        else:
            keywords_list.append(keywords.strip())
        print(keywords_list)
        # jobs = await get_linkedin_job_recommendations(
        #     keywords_list, location
        # )
        # jobs = {
        #     "jobs": [
        #         {
        #             "title": "Software Engineer",
        #             "company": "Tech Company",
        #             "location": "Remote",
        #             "description": "Develop and maintain software applications.",
        #             "url": "https://www.linkedin.com/jobs/view/1234567890"
        #         },
        #         {
        #             "title": "Data Scientist",
        #             "company": "Data Solutions Inc.",
        #             "location": "New York, NY",
        #             "description": "Analyze data to drive business decisions.",
        #             "url": "https://www.linkedin.com/jobs/view/0987654321"
        #         }
        #     ]
        #     }
        logger.info("Jobs from LinkedIn fetched successfully!")

        # with open("linkedin.json", "w") as f:
        #     f.write(str(jobs))
        try:
            with open("artifacts/linkedin.json","r") as f:
                jobs = f.read()

            jobs = make_data_clean(jobs)
        
        except Exception as e:
            logger.error(f"Error while cleaning job: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

        # request object pass karna mandatory hai
        return templates.TemplateResponse(
            "linkedin.html",
            {"request": request, "jobs": jobs}
        )
    except Exception as e:
        logger.error(f"Error while searching job from the linkedin: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
  

@router.get("/job-recommendation/naukri")
async def naukri_jobs(request: Request, keywords: str = "", location: str = ""):
    try:
        # print(keywords)
        # print(location)
        # keywords_list = []
        # if "," in keywords:
        #     keywords_list.extend([kw.strip() for kw in keywords.split(",")])
        # else:
        #     keywords_list.append(keywords.strip())
        # print(keywords_list)
        jobs = await get_naukri_job_recommendations(keywords, location)
        # print(jobs)
        # return JSONResponse(content=jobs)
        with open("naukri.json", "w") as f:
            f.write(str(jobs))

        logger.info("Jobs from naukri fetched successfully!")
        return templates.TemplateResponse(
            "jobs.html", 
            {"request": request,"jobs": jobs}
        )

    except Exception as e:
        logger.error(f"Error while searching job from the naukri: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

 