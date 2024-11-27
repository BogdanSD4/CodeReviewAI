import json
import os

from abc import ABC, abstractmethod

from openai import OpenAI

from src.models import ReviewRequest
from src.utils.github_manager import GithubRepo
from src.redis_config import redis_client
import src.utils.func as utils


class AiApi(ABC):
    def __init__(self, review: ReviewRequest):
        self.repo_description: str = review.assignment_description
        self.dev_level: str = review.candidate_level
        self.git: GithubRepo = GithubRepo(review.github_repo_url)

        self.key = utils.get_hash(f'{self.git.owner}{self.git.repo_name}{self.dev_level}')
        self.cache = redis_client.get_key(self.key)

    @abstractmethod
    def get_prompt(self, data: str) -> str:
        return ''

    @abstractmethod
    def analyze_branch(self, data: str):
        pass


class GptApi(AiApi):
    def __init__(self, review: ReviewRequest):
        super().__init__(review)
        self.client = OpenAI(api_key=os.environ.get('GPTCHAT_API'))

    def get_prompt(self, data: str) -> str:
        return f"""
            short description of the repository:
            {self.repo_description}
            Developer level: {self.dev_level}
            
            You are a professional code reviewer. Analyze this repository and return the following:
            - Cons/Comments: What are the drawbacks or comments about this repository?
            - Rating: Rate the repository based on documentation, code quality, and functionality (1-10 for each category according to developer level).
            - Conclusion: What are the conclusions and recommendations for this repository?
            
            Repository structure and content:
            {data}
            """

    def analyze_branch(self, data):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": self.get_prompt(data)}],
        )

        return response.choices[0].message.content

    def analyze(self):
        if self.cache:
            return json.loads(self.cache)

        result = []
        for branch in self.git.branches:
            branch_dict = branch.get_dict()
            result.append({
                'branch': branch_dict,
                'analyze': self.analyze_branch(json.dumps(branch_dict))
            })

        redis_client.set_key(self.key, json.dumps(result))

        return result

