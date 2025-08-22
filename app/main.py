from app.routers import job_recommendation 
from app.routers import suggestions 
from app import cache
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from services.redis_config import RedisConfig
from services.session_manager import SessionManager
from contextlib import asynccontextmanager
from jobRecommender import logger


# Global objects
redis_config = RedisConfig()
session_manager: SessionManager = None # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting the Job Recommendation")
    try:
        client = await redis_config.init()
        global session_manager
        session_manager = SessionManager(client)
        logger.info("Redis client initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Redis client: {e}")
        raise e

    yield

    try:
        await redis_config.close()
        logger.info("Redis client closed successfully")
    except Exception as e:
        logger.error(f"Error closing Redis client: {e}")
    logger.info("Job Recommendation application is shutting down")

app = FastAPI(lifespan=lifespan)



# Tell FastAPI where templates are
templates = Jinja2Templates(directory="app/templates")  

app.mount("/static", StaticFiles(directory="./app/templates/static", html=True), name="static")



app.include_router(job_recommendation.router)
app.include_router(suggestions.router)

@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

