import os

import requests

from fastapi import APIRouter, Response, Request, Form
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.utils.github_manager import GithubRepo
from src.models import ReviewRequest
from src.ai.gpt_api import GptApi

router = APIRouter(prefix="/api", tags=["API"])


@router.post("/review/")
async def repo_review(request: Request):
    form = await request.form(),
    form = dict(form[0])

    try:
        review = ReviewRequest(**form)

        git = GithubRepo(review.github_repo_url)

        gpt_ai = GptApi(review)

        # print(f'{response.content=}')
        # if response.status_code == 200:
        #     data = response.json()
        #     for file in data['tree']:
        #         print(f"File: {file['path']} | Type: {file['type']} | SHA: {file['sha']}")

        return JSONResponse(content={
            "status": "success",
            "review_data": review.dict(),
            "review": gpt_ai.analyze()
        }, status_code=200)
    except ValidationError as e:
        return JSONResponse(content={"status": "error", "errors": e.errors()}, status_code=422)
