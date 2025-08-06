from pydantic import BaseModel, Field
from typing import List, Optional, Any



class ResumeSummary(BaseModel):
    """
    Represents a summary of the candidate's resume.
    """
    summary: str = Field(..., description="Summary of the candidate's professional profile and career objectives")
    
   
class Keywords(BaseModel):
    """
    Represents keywords used for job recommendations.
    """
    keywords: List[str] = Field(..., description="List of most suited keywords for job recommendations based on skills and experience")


class FindSkillGap(BaseModel):
    """
    Represents the skill gap analysis.
    """
    analysis: str = Field(..., description="Analysis of the candidate's missing skills and recommendations for improvement")

class ProjectIdeas(BaseModel):
    """
    Represents project ideas based on the candidate's skills.
    """
    ideas: str = Field(..., description="Project ideas that can be added to the resume to enhance the candidate's profile")

class ImprovementAreas(BaseModel):
    """
    Represents areas of improvement for the candidate.
    """
    suggestions: str = Field(..., description="Suggestions for improving the resume to increase job opportunities")