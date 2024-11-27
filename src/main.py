from dotenv import load_dotenv
from fastapi import FastAPI

from src.routes import views

load_dotenv()

app = FastAPI(
    title="CodeReviewAl",
    description="The service should integrate the OpenAl API (or alternative API) for code analysis and the GitHub API for accessing the repository.",
)

app.include_router(views.router)

