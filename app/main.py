from app.routers import job_recommendation 
from app.routers import suggestions 
from fastapi import FastAPI

app = FastAPI()

app.include_router(job_recommendation.router)
app.include_router(suggestions.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Job Recommender API"}