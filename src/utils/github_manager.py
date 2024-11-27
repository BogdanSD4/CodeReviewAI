import base64
import os
import re
from typing import List

import requests


class GitTreeNode:
    def __init__(self, data):
        self.name: str = data['path']
        self.data: str or None = None
        self.children = []

        response = requests.get(data['url'], headers=GithubRepo.headers).json()

        if data['type'] == 'tree':
            if self.name not in ['.vs']:
                self.children = [GitTreeNode(node) for node in response['tree']]
        elif data['type'] == 'blob':
            not_allowed = ['.git', '.svn', '.dll', '.cache']
            if not any(self.name.endswith(item) for item in not_allowed):
                decoded_bytes = base64.b64decode(response['content'])
                self.data = decoded_bytes.decode('utf-8', errors='replace')

    def get_dict(self):
        result = {
            'name': self.name,
            'children': [child.get_dict() for child in self.children]
        }

        if self.data is not None:
            result['data'] = self.data

        return result


class GithubRepo:
    headers = {
        'Authorization': f'token {os.environ.get('GITHUB_API')}',
    }

    def __init__(self, url: str):
        self.api_url = 'https://api.github.com/'
        self.url = url

        valid = self.get_repo_owner()
        if valid:
            self.owner = valid['owner']
            self.repo_name = valid['repo']

        response = requests.get(f'{self.api_url}repos/{self.owner}/{self.repo_name}/branches', headers=self.headers).json()
        self.branches: list[GitBranch] = [GitBranch(self, branch) for branch in response]

    @staticmethod
    def valid_url(url: str):
        pattern = r"https://github\.com/(?P<owner>[\w-]+)/(?P<repo>[\w-]+)"
        return re.match(pattern, url)

    def get_repo_owner(self) -> dict:
        match = self.valid_url(self.url)

        if match:
            return {"owner": match.group("owner"), "repo": match.group("repo")}
        else:
            raise Exception("Invalid url")


class GitBranch:
    def __init__(self, repo: GithubRepo, data):
        self.repo = repo
        self.name: str = data.get('name', '')
        self.protected: str = data.get('protected', '')
        self.tree: list[GitTreeNode] = self.get_tree()

    def get_tree(self) -> list[GitTreeNode]:
        response = requests.get(f'{self.repo.api_url}repos/{self.repo.owner}/{self.repo.repo_name}/git/trees/{self.name}', headers=GithubRepo.headers).json()
        return [GitTreeNode(node) for node in response['tree']]

    def get_dict(self):
        return {
            'name': self.name,
            'files': [node.get_dict() for node in self.tree]
        }
