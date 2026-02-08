from typing import Optional, List, Literal, Dict
from pydantic import BaseModel

class GitHubScanRequest(BaseModel):
    """Request body from frontend containing the GitHub repo URL."""
    repo_url: str

class InputRepository(BaseModel):
    """Repository identifier used across the pipeline.
    - owner: GitHub owner/org
    - name: repository name
    - ref: branch or ref to scan (default 'main')
    - subpath: optional sub-directory within the repo to restrict scanning
    """
    owner: str
    name: str
    ref: Optional[str] = "main"
    subpath: Optional[str] = None

class SourceFile(BaseModel):
    """A single source file collected by the ingestion step."""
    path: str      # repository path (relative to repo or subpath)
    content: str   # file text content

class FilesMetadata(BaseModel):
    """Optional metadata produced during repo fetch step."""
    truncated: bool = False
    reason: Optional[str] = None

class FilesPayload(BaseModel):
    """Payload shape to pass from the fetch layer to the scanner engine.
    - repo: InputRepository
    - files: list of SourceFile
    - metadata: optional info if files were truncated/skipped
    """
    repo: InputRepository
    files: List[SourceFile]
    metadata: Optional[FilesMetadata] = None

class Finding(BaseModel):
    """A minimal finding model for Phase-2 (keeps things easy for the UI).
    - id: unique id within this scan (string)
    - path: repo-relative path to file
    - line: 1-based line number (optional)
    - rule_id: which rule matched
    - secret_type: best-effort label (e.g., 'GH_PAT')
    - severity: low|medium|high
    - confidence: optional confidence label
    - snippet_redacted: short redacted context
    - message: short human-friendly explanation
    - remediation: optional remediation suggestion
    """
    id: Optional[str] = None
    path: str
    line: Optional[int] = None
    rule_id: str
    secret_type: Optional[str] = None
    severity: Literal["low", "medium", "high"] = "medium"
    confidence: Optional[Literal["LOW", "MEDIUM", "HIGH"]]
    snippet_redacted: Optional[str] = None
    message: Optional[str] = None
    remediation: Optional[str] = None
    meta: Optional[Dict[str, str]] = None

class Stats(BaseModel):
    """Simplified ingestion statistics for Phase-2 UI.
    Only include minimal counters to keep the UI simple for beginners.
    """
    files_considered: int = 0        # total archive entries examined
    files_included: int = 0          # files that passed filters and were candidates
    files_read: int = 0              # files actually read into memory

class ScanResponse(BaseModel):
    """Phase-2 scan response shape (minimal).
    - ok: whether the scan completed without an error
    - repo: echo of the scanned repo meta
    - stats: simplified ingestion stats
    - findings: list of Finding (empty if stub)
    - error: optional human-friendly error message when ok is false
    """
    ok: bool = True
    repo: Optional[InputRepository] = None
    stats: Stats = Stats()
    findings: List[Finding] = []
    error: Optional[str] = None