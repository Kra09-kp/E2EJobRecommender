from app.model.ask_llm import AskLLM
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jobRecommender import logger
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import UploadFile, File
import json
from pdfminer.high_level import extract_text
from io import BytesIO
from app.cache.suggestions_cache import SuggestionsCache

templates = Jinja2Templates(directory="app/templates")  

router = APIRouter()
ask_llm = AskLLM()


class ResumeData(BaseModel):
    resume_text: str

@router.post("/suggestions")
async def get_suggestions(request: Request, resume_file: UploadFile = File(...)):
    try:
        from app.main import session_manager
        session_id = request.cookies.get("session_id")
        suggestion_cache = SuggestionsCache(session_manager)
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required in headers")
        
        if not resume_file.filename.endswith(".pdf"):  # type: ignore
            logger.error("Only PDF files are allowed")
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        file_content = await resume_file.read()
        resume_text = extract_text(BytesIO(file_content))
        
        # check if the data already save if yes then just load
        cached_suggestions = await suggestion_cache.get(session_id,resume_text[:15].encode())
        if cached_suggestions:
            print("Suggestions are already generated on this resume. Here is the cached version")
            return templates.TemplateResponse(
            "suggestion.html",
            {"request": request,
             "suggestion":cached_suggestions}
        ) 
            
       
        # suggestions = ask_llm.get_suggestion(resume_text)

        # print(suggestions)
        logger.info("Suggestion generated successfully")
        with open('artifacts/suggestion.json','r') as f:
            suggestions = f.read()
        suggestions = json.loads(suggestions)

        logger.info("🔍 No cache found, saving suggestions...")
        # Save in Redis
        await suggestion_cache.save(session_id,resume_text[:15].encode(), suggestions)
        logger.info("✅ Saved suggestions to cache")
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
    

