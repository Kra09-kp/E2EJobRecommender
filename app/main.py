from app.routers import job_recommendation 
from app.routers import suggestions 
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Tell FastAPI where templates are
templates = Jinja2Templates(directory="app/templates")  

app.mount("/static", StaticFiles(directory="./app/templates/static", html=True), name="static")



app.include_router(job_recommendation.router)
app.include_router(suggestions.router)

@app.get("/",response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
