from typing import Optional, List, Literal
from pydantic import BaseModel


Severity = Literal["low", "medium", "high"]


class Finding(BaseModel):
    rule_id: str
    severity: Severity
    message: str
    line: Optional[int] = None
    snippet: Optional[str] = None


class ScanResponse(BaseModel):
    findings: List[Finding]
