#endpoint

from fastapi import APIRouter, HTTPException
from models.contracts import Finding, GitHubScanRequest, ScanResponse
from urllib.parse import urlparse

scan_router = APIRouter()

@scan_router.post("/github", response_model=ScanResponse)
def scan_GitHub(request: GitHubScanRequest):

    repo_url = request.repo_url

    try:
        normalize_Url(repo_url)
    except InvalidGitHubRepoUrl as e:
        raise HTTPException(status_code=400, detail=str(e))

    return { "findings": []}
class InvalidGitHubRepoUrl(ValueError):
    pass

def normalize_Url(repo_url: str) -> str:
    
    if not repo_url or not repo_url.strip():
        raise InvalidGitHubRepoUrl("Empty URL")

    url = repo_url.strip()

    if not url.startswith(("https://")): #if url doesn't start with https://, add it
        url = "https://" + url

    parsed = urlparse(url)

    if parsed.netloc != "github.com":#github repo input only
        raise InvalidGitHubRepoUrl("Only github.com repo URLs are supported")

    if parsed.query or parsed.fragment: # Reject query strings or fragments
        raise InvalidGitHubRepoUrl("Invalid GitHub repo URL")

    path = parsed.path.rstrip("/") #Normalize path
    if path.endswith(".git"):
        path = path[:-4]
    parts = path.lstrip("/").split("/")

    # Must be exactly /owner/repo
    if len(parts) != 2:
        raise InvalidGitHubRepoUrl("URL must be a GitHub repository root (https://github.com/owner/repo)")
    owner, repo = parts

    if not owner or not repo:
        raise InvalidGitHubRepoUrl("Invalid GitHub repo URL")

    return f"https://github.com/{owner}/{repo}"
