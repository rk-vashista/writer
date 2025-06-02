from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import json
import os
import base64
from urllib.parse import urlparse

class GithubRepoInput(BaseModel):
    """Input schema for GitHub repository tool."""
    repo_url: str = Field(..., description="URL of the GitHub repository")
    content_type: str = Field(..., description="Type of content to generate (description or tags)")

class GithubRepoTool(BaseTool):
    name: str = "GitHub Repository Analyzer"
    description: str = (
        "Tool for analyzing GitHub repositories and generating descriptions or tags. "
        "This tool can fetch repository information and analyze its contents."
    )
    args_schema: Type[BaseModel] = GithubRepoInput

    def _run(self, repo_url: str, content_type: str) -> str:
        try:
            # Parse the repo URL to get owner and repo name
            path_parts = urlparse(repo_url).path.strip('/').split('/')
            if len(path_parts) < 2:
                return "Invalid GitHub repository URL"
            owner, repo = path_parts[-2:]
            
            # Get GitHub token from environment
            github_token = os.getenv('GITHUB_TOKEN')
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"token {github_token}" if github_token else None
            }
            
            # Fetch repository information
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            repo_response = requests.get(api_url, headers=headers)
            
            if repo_response.status_code == 404:
                return "Repository not found or is private"
            elif repo_response.status_code != 200:
                return f"Error accessing repository: {repo_response.status_code}"
            
            repo_data = repo_response.json()
            
            # Additional data collection based on content type
            if content_type.lower() == "description":
                languages_url = repo_data['languages_url']
                languages_response = requests.get(languages_url, headers=headers)
                languages = languages_response.json() if languages_response.status_code == 200 else {}
                
                # Get README content
                readme_url = f"{api_url}/readme"
                readme_response = requests.get(readme_url, headers=headers)
                readme_content = ""
                if readme_response.status_code == 200:
                    readme_data = readme_response.json()
                    readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
                
                return json.dumps({
                    "name": repo_data['name'],
                    "description": repo_data['description'],
                    "languages": languages,
                    "stars": repo_data['stargazers_count'],
                    "forks": repo_data['forks_count'],
                    "open_issues": repo_data['open_issues_count'],
                    "topics": repo_data.get('topics', []),
                    "readme": readme_content[:1000] if readme_content else ""  # First 1000 chars
                })
            
            elif content_type.lower() == "tags":
                # Get repository topics and generate relevant tags
                return json.dumps({
                    "topics": repo_data.get('topics', []),
                    "language": repo_data['language'],
                    "stars": repo_data['stargazers_count'],
                    "is_template": repo_data['is_template'],
                    "has_wiki": repo_data['has_wiki'],
                    "has_pages": repo_data['has_pages']
                })
            
            return "Invalid content type specified"
            
        except Exception as e:
            return f"Error analyzing repository: {str(e)}"
