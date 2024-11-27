from pydantic import ValidationError
import pytest
from src.models import ReviewRequest


def test_valid_github_url():
    request_data = {
        "assignment_description": "Test description",
        "github_repo_url": "https://github.com/owner/repo",
        "candidate_level": "junior"
    }
    request = ReviewRequest(**request_data)
    assert request.github_repo_url == "https://github.com/owner/repo"


def test_invalid_github_url_prefix():
    request_data = {
        "assignment_description": "Test description",
        "github_repo_url": "https://gitlab.com/owner/repo",
        "candidate_level": "junior"
    }
    with pytest.raises(ValidationError) as exc_info:
        ReviewRequest(**request_data)

    assert "The URL must start with 'https://github.com/'" in str(exc_info.value)


def test_invalid_github_url_format():
    request_data = {
        "assignment_description": "Test description",
        "github_repo_url": "https://github.com/",
        "candidate_level": "junior"
    }
    with pytest.raises(ValidationError) as exc_info:
        ReviewRequest(**request_data)

    assert "The URL must include both an owner and a repository name." in str(exc_info.value)


def test_invalid_candidate_level():
    request_data = {
        "assignment_description": "Test description",
        "github_repo_url": "https://github.com/owner/repo",
        "candidate_level": "expert"
    }
    with pytest.raises(ValidationError) as exc_info:
        ReviewRequest(**request_data)

    assert "Input should be 'junior', 'middle' or 'senior'" in str(exc_info.value)
