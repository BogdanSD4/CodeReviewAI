from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from src.utils.github_manager import GithubRepo


class ReviewRequest(BaseModel):
    assignment_description: str = Field(..., max_length=200, description='Description of the git repo')
    github_repo_url: str = Field(...)
    candidate_level: Literal['junior', 'middle', 'senior']

    @field_validator("github_repo_url")
    @classmethod
    def validate_github_url(cls, value) -> str:
        if not value.startswith("https://github.com/"):
            raise ValueError("The URL must start with 'https://github.com/'")
        elif not GithubRepo.valid_url(value):
            raise ValueError("The URL must include both an owner and a repository name.")
        return value