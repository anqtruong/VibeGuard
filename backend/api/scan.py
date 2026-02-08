#endpoint

from fastapi import APIRouter, HTTPException
from models.contracts import Finding, GitHubScanRequest, ScanResponse, InputRepository
from urllib.parse import urlparse

class InvalidGitHubRepoUrl(ValueError):
    pass

scan_router = APIRouter()
@scan_router.post("/github", response_model=ScanResponse)
def scan_GitHub(request: GitHubScanRequest):

    repo_url = request.repo_url

    try:
        normalize_Url(repo_url)
    except InvalidGitHubRepoUrl as e:
        raise HTTPException(status_code=400, detail=str(e))

    return { "findings": []}

def normalize_Url(repo_url: str) -> InputRepository:
    # basic validation
    if not repo_url or not repo_url.strip():
        raise InvalidGitHubRepoUrl("Empty URL")

    url = repo_url.strip()

    if not url.startswith(("https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if parsed.netloc != "github.com":
        raise InvalidGitHubRepoUrl("Only github.com repo URLs are supported")

    if parsed.query or parsed.fragment:
        raise InvalidGitHubRepoUrl("Invalid GitHub repo URL")

    path = parsed.path.rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]

    parts = path.lstrip("/").split("/")

    # require at least /owner/repo
    if len(parts) < 2:
        raise InvalidGitHubRepoUrl("URL must be a GitHub repository (https://github.com/owner/repo)")

    owner = parts[0]
    name = parts[1]

    # default ref
    ref = "main"
    subpath = None

    # support /owner/repo/tree/{ref}/optional/subpath
    if len(parts) >= 3:
        if parts[2] == "tree":
            if len(parts) < 4:
                raise InvalidGitHubRepoUrl("Invalid repository URL; missing branch after /tree/")
            ref = parts[3] or "main"
            if len(parts) > 4:
                subpath = "/".join(parts[4:])
        else:
            # disallow other repo subpaths (issues, pulls, etc.)
            raise InvalidGitHubRepoUrl("URL must be a GitHub repository root or tree URL")

    return InputRepository(owner=owner, name=name, ref=ref, subpath=subpath)
