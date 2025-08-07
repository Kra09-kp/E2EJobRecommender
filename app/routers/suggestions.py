from app.model.ask_llm import AskLLM
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Dict, Any

router = APIRouter()
ask_llm = AskLLM()


class ResumeRequest(BaseModel):
    resume_text: str

@router.post("/suggestions")
async def get_suggestions(request: ResumeRequest):
    """
    Get suggestions based on the resume text.
    """
    try:
        suggestions = ask_llm.get_suggestion(request)
        print(suggestions)
        return JSONResponse(content={"Suggestions":suggestions})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
