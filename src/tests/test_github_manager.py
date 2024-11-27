import pytest
import requests
from unittest.mock import patch

from src.tests.mocks import MockResponse
from src.utils.github_manager import GithubRepo, GitBranch, GitTreeNode


@pytest.fixture
def mock_requests_get(monkeypatch):
    def mock_get(url, headers=None):
        if 'branches' in url:
            return MockResponse([{'name': 'main', 'protected': False}], 200)
        elif 'git/trees/main' in url:
            return MockResponse({'tree': [{'path': 'file1.py', 'type': 'blob', 'url': 'mock_url_blob'}]}, 200)
        elif 'mock_url_blob' in url:
            return MockResponse({'content': 'cHJpbnQoIkhlbGxvIFdvcmxkIik='}, 200)  # base64("print("Hello World")")
        return MockResponse({}, 404)

    monkeypatch.setattr(requests, "get", mock_get)


def test_github_repo_initialization(mock_requests_get):
    url = "https://github.com/user/repo"
    repo = GithubRepo(url)

    assert repo.owner == "user"
    assert repo.repo_name == "repo"
    assert len(repo.branches) == 1
    assert repo.branches[0].name == "main"


def test_git_branch_initialization(mock_requests_get):
    url = "https://github.com/user/repo"
    repo = GithubRepo(url)
    branch = repo.branches[0]

    assert branch.name == "main"
    assert len(branch.tree) == 1
    assert branch.tree[0].name == "file1.py"


def test_invalid_url():
    with pytest.raises(Exception, match="Invalid url"):
        GithubRepo("https://invalid_url.com/user/repo")


def test_invalid_api_response(monkeypatch):
    def mock_get(mock_url, headers=None):
        return MockResponse({'url': mock_url, 'headers': headers}, 404)

    monkeypatch.setattr(requests, "get", mock_get)

    url = "https://github.com/user/repo"
    with pytest.raises(Exception):
        repo = GithubRepo(url)
        repo.get_repo_owner()
