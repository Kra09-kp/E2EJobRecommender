from app.model.ask_llm import AskLLM
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from jobRecommender import logger
from jobRecommender.utils.helper import make_data_clean
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi import UploadFile, File
import json
from pdfminer.high_level import extract_text
from io import BytesIO

templates = Jinja2Templates(directory="app/templates")  

router = APIRouter()
ask_llm = AskLLM()


class ResumeData(BaseModel):
    resume_text: str

@router.post("/suggestions")
async def get_suggestions(request: Request, resume_file: UploadFile = File(...)):
    try:
        if not resume_file.filename.endswith(".pdf"):  # type: ignore
            logger.error("Only PDF files are allowed")
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        file_content = await resume_file.read()
        resume_text = extract_text(BytesIO(file_content))
        
        # suggestions = ask_llm.get_suggestion(resume_text)

        # print(suggestions)
        logger.info("Suggestion generated successfully")
        with open('artifacts/suggestion.json','r') as f:
            suggestions = f.read()
        suggestions = json.loads(suggestions)

        # print(suggestions)
        # return JSONResponse(content={"Suggestions":suggestions})
        return templates.TemplateResponse(
            "suggestion.html",
            {"request": request,
             "suggestion":suggestions}
        ) 
    except Exception as e:
        logger.error("Error while generating suggestion",str(e))
        raise HTTPException(status_code=500, detail=str(e))
    

