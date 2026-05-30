from typing import Optional, List, Literal
from pydantic import BaseModel

class GitHubScanRequest(BaseModel): #This is where our input repo url is stored
    repo_url: str
class Finding(BaseModel):
    """Represents a single vulnerability finding from the scanner."""
    rule_id: str
    severity: Literal["low", "medium", "high"]
    message: str
    path: Optional[str] = None
    line: Optional[int] = None
    snippet: Optional[str] = None

class ScanResponse(BaseModel): #Return list of findings
    findings: List[Finding]

class InputRepository(BaseModel):
    owner: str
    name: str
    ref: Optional[str] = "main"     # branch/ref to scan (default "main")
    subpath: Optional[str] = None   # optional sub-directory within the repo

class SourceFile(BaseModel):
    path: str      # repository path (relative)
    content: str   # full file content (text)
