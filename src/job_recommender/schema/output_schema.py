from pydantic import BaseModel, Field

class ResumeSummary(BaseModel):
    """
    Represents a summary of a resume.
    """
    name: str = Field(..., description="Name of the candidate")
    skills: list[str] = Field(..., description="List of skills possessed by the candidate")
    experience: list[str] = Field(..., description="List of experiences of the candidate")
    education: list[str] = Field(..., description="List of educational qualifications of the candidate")

class Keywords(BaseModel):
    """
    Represents keywords used for job recommendations.
    """
    keywords: list[str] = Field(..., description="List of most suited keywords for job recommendations based on skills and experience")


class FindSkillGap(BaseModel):
    """
    Represents the skill gap analysis.
    """
    skill_gap: list[str] = Field(..., description="List of skills that are missing or need improvement for the candidate")
    recommendations: list[str] = Field(..., description="List of recommendations to fill the skill gap")

class ProjectIdeas(BaseModel):
    """
    Represents project ideas based on the candidate's skills.
    """
    ideas: list[str] = Field(..., 
                    description="List of project ideas that can be implemented based on the candidate's skills to enhance their portfolio")


class ImprovementAreas(BaseModel):
    """
    Represents areas of improvement for the candidate.
    """
    areas: list[str] = Field(..., description="List of areas where the candidate can improve their skills or knowledge")
    suggestions: list[str] = Field(..., description="List of suggestions to improve in the identified areas")