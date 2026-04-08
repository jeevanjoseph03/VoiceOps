from github import Github
from app.core.config import settings

def get_latest_commit_logic(repo_name: str) -> str:
    """Core logic to fetch the latest commit from GitHub."""
    if not settings.GITHUB_TOKEN:
        return "Error: GITHUB_TOKEN is not configured in the environment."
        
    try:
        # Initialize GitHub client
        g = Github(settings.GITHUB_TOKEN)
        
        # Fetch the repository
        repo = g.get_repo(repo_name)
        
        # Get the latest commit from the default branch
        latest_commit = repo.get_commits()[0]
        
        author = latest_commit.commit.author.name
        message = latest_commit.commit.message
        sha = latest_commit.sha[:7]
        
        return f"The latest commit in {repo_name} was by {author}. Commit message: '{message}'. Commit Hash: {sha}."
        
    except Exception as e:
        return f"Failed to fetch commit from GitHub. Error details: {str(e)}"