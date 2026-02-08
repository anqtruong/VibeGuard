#endpoint

from fastapi import APIRouter, HTTPException
from models.contracts import Finding, GitHubScanRequest, ScanResponse, InputRepository, Stats
from urllib.parse import urlparse

from scanner.ingest import ingest_repo, NotFoundError, DownloadTimeout, TooLargeError, IngestError

class InvalidGitHubRepoUrl(ValueError):
    pass

scan_router = APIRouter()

@scan_router.post("/github", response_model=ScanResponse)
async def scan_GitHub(request: GitHubScanRequest):
    # validate and parse repo URL into structured InputRepository
    try:
        repo_meta = normalize_Url(request.repo_url)
    except InvalidGitHubRepoUrl as e:
        raise HTTPException(status_code=400, detail=str(e))

    # call ingestion to fetch files (anonymous download)
    try:
        payload, stats = await ingest_repo(repo_meta.owner, repo_meta.name, ref=repo_meta.ref, subpath=repo_meta.subpath, timeout=30)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except DownloadTimeout as e:
        raise HTTPException(status_code=504, detail=str(e))
    except TooLargeError as e:
        raise HTTPException(status_code=413, detail=str(e))
    except IngestError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    # return minimal ScanResponse with empty findings (scanner stub)
    return ScanResponse(ok=True, repo=repo_meta, stats=stats, findings=[])

# minimal URL normalizer that returns structured InputRepository
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
            raise InvalidGitHubRepoUrl("URL must be a GitHub repository root or tree URL")

    return InputRepository(owner=owner, name=name, ref=ref, subpath=subpath)
