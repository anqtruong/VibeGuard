## Finding
- rule_id: string (required)
- severity: "low" | "medium" | "high"
- message: string (required)
- path: string (optional)
- line: number (optional)
- snippet: string (optional)

## GitHubScanRequest
{
  "findings": [Finding]
}

## Notes
- This contract is a guideline for a solo project; amendments are allowed when discussed
- New optional fields may be added
- Removed: location (was redundant with line)
