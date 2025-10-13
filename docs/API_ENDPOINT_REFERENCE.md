# InsightVM API v3 Endpoint Reference

## Quick Reference Guide

This document provides a quick reference for all InsightVM API v3 endpoints used in the insightvm-python library, verified against the official Rapid7 API documentation.

**Last Updated:** 2025-10-13  
**API Version:** 3  
**Base URL Format:** `{base_url}/api/3/{endpoint}`

---

## Endpoint Naming Convention

⚠️ **IMPORTANT:** InsightVM API v3 uses **underscores** (_) not hyphens (-) for multi-word endpoint names.

✅ **Correct:** `/api/3/scan_engines`  
❌ **Incorrect:** `/api/3/scan-engines`

---

## Core Endpoints

### Assets
```
GET    /api/3/assets                    - List all assets
GET    /api/3/assets/{id}               - Get specific asset
POST   /api/3/assets/search             - Search assets with criteria
GET    /api/3/assets/{id}/vulnerabilities - Get asset vulnerabilities
GET    /api/3/assets/{id}/software      - Get installed software
GET    /api/3/assets/{id}/tags          - Get asset tags
PUT    /api/3/assets/{id}/tags/{tagId}  - Add tag to asset
DELETE /api/3/assets/{id}/tags/{tagId}  - Remove tag from asset
```

**Module:** `src/rapid7/api/assets.py`  
**Client Access:** `client.assets`

---

### Asset Groups
```
GET    /api/3/asset_groups              - List all asset groups
POST   /api/3/asset_groups              - Create asset group
GET    /api/3/asset_groups/{id}         - Get specific group
PUT    /api/3/asset_groups/{id}         - Update asset group
DELETE /api/3/asset_groups/{id}         - Delete asset group
GET    /api/3/asset_groups/{id}/assets  - Get assets in group
PUT    /api/3/asset_groups/{id}/assets/{assetId} - Add asset to group
DELETE /api/3/asset_groups/{id}/assets/{assetId} - Remove asset from group
```

**Module:** `src/rapid7/api/asset_groups.py`  
**Client Access:** `client.asset_groups`

---

### Sites
```
GET    /api/3/sites                     - List all sites
POST   /api/3/sites                     - Create site
GET    /api/3/sites/{id}                - Get specific site
PUT    /api/3/sites/{id}                - Update site
DELETE /api/3/sites/{id}                - Delete site
GET    /api/3/sites/{id}/assets         - Get site assets
GET    /api/3/sites/{id}/scan_engine    - Get site scan engine
PUT    /api/3/sites/{id}/scan_engine    - Set site scan engine
GET    /api/3/sites/{id}/scan_template  - Get site scan template
PUT    /api/3/sites/{id}/scan_template  - Set site scan template
POST   /api/3/sites/{id}/scans          - Start site scan
GET    /api/3/sites/{id}/scans          - List site scans
```

**Module:** `src/rapid7/api/sites.py`  
**Client Access:** `client.sites`

---

### Scans
```
GET    /api/3/scans                     - List all scans
GET    /api/3/scans/{id}                - Get specific scan
POST   /api/3/scans/{id}/stop           - Stop scan
POST   /api/3/scans/{id}/pause          - Pause scan
POST   /api/3/scans/{id}/resume         - Resume scan
POST   /api/3/sites/{id}/scans          - Start site scan
```

**Module:** `src/rapid7/api/scans.py`  
**Client Access:** `client.scans`

---

### Scan Engines
```
GET    /api/3/scan_engines              - List all scan engines
POST   /api/3/scan_engines              - Create scan engine
GET    /api/3/scan_engines/{id}         - Get specific engine
PUT    /api/3/scan_engines/{id}         - Update scan engine
DELETE /api/3/scan_engines/{id}         - Delete scan engine
GET    /api/3/scan_engines/{id}/sites   - Get engine sites
GET    /api/3/scan_engines/{id}/scans   - Get engine scans
GET    /api/3/scan_engines/shared_secret - Get shared secret
POST   /api/3/scan_engines/shared_secret - Create shared secret
DELETE /api/3/scan_engines/shared_secret - Revoke shared secret
```

**Module:** `src/rapid7/api/scan_engines.py`  
**Client Access:** `client.scan_engines`

---

### Scan Engine Pools
```
GET    /api/3/scan_engine_pools         - List all engine pools
POST   /api/3/scan_engine_pools         - Create engine pool
GET    /api/3/scan_engine_pools/{id}    - Get specific pool
PUT    /api/3/scan_engine_pools/{id}    - Update engine pool
DELETE /api/3/scan_engine_pools/{id}    - Delete engine pool
GET    /api/3/scan_engine_pools/{id}/engines - Get pool engines
PUT    /api/3/scan_engine_pools/{id}/engines - Set pool engines
PUT    /api/3/scan_engine_pools/{id}/engines/{engineId} - Add engine to pool
DELETE /api/3/scan_engine_pools/{id}/engines/{engineId} - Remove engine from pool
```

**Module:** `src/rapid7/api/scan_engines.py`  
**Client Access:** `client.scan_engines` (pool methods)

---

### Scan Templates
```
GET    /api/3/scan_templates            - List all templates
GET    /api/3/scan_templates/{id}       - Get specific template
```

**Module:** `src/rapid7/api/scan_templates.py`  
**Client Access:** `client.scan_templates`

---

### Reports
```
GET    /api/3/reports                   - List all reports
POST   /api/3/reports                   - Create report
GET    /api/3/reports/{id}              - Get specific report
PUT    /api/3/reports/{id}              - Update report
DELETE /api/3/reports/{id}              - Delete report
POST   /api/3/reports/{id}/generate     - Generate report
GET    /api/3/reports/{id}/history      - Get report history
GET    /api/3/reports/{id}/history/{instance}/output - Download report
```

**Module:** `src/rapid7/api/reports.py`  
**Client Access:** `client.reports`

---

### Vulnerabilities
```
GET    /api/3/vulnerabilities           - List all vulnerabilities
GET    /api/3/vulnerabilities/{id}      - Get specific vulnerability
GET    /api/3/vulnerabilities/{id}/affected_assets - Get affected assets
GET    /api/3/vulnerabilities/{id}/exploits - Get exploits
GET    /api/3/vulnerabilities/{id}/malware_kits - Get malware kits
GET    /api/3/vulnerabilities/{id}/references - Get references
GET    /api/3/vulnerabilities/{id}/solutions - Get solutions
```

**Module:** `src/rapid7/api/vulnerabilities.py`  
**Client Access:** `client.vulnerabilities`

---

### Vulnerability Exceptions
```
GET    /api/3/vulnerability_exceptions  - List all exceptions
POST   /api/3/vulnerability_exceptions  - Create exception
GET    /api/3/vulnerability_exceptions/{id} - Get specific exception
DELETE /api/3/vulnerability_exceptions/{id} - Delete exception
POST   /api/3/vulnerability_exceptions/{id}/approve - Approve exception
POST   /api/3/vulnerability_exceptions/{id}/reject - Reject exception
```

**Module:** `src/rapid7/api/vulnerability_exceptions.py`  
**Client Access:** `client.vulnerability_exceptions`

---

### Solutions
```
GET    /api/3/solutions                 - List all solutions
GET    /api/3/solutions/{id}            - Get specific solution
```

**Module:** `src/rapid7/api/solutions.py`  
**Client Access:** `client.solutions`

---

### Sonar Queries
```
GET    /api/3/sonar_queries             - List all queries
POST   /api/3/sonar_queries             - Create query
GET    /api/3/sonar_queries/{id}        - Get specific query
PUT    /api/3/sonar_queries/{id}        - Update query
DELETE /api/3/sonar_queries/{id}        - Delete query
```

**Module:** `src/rapid7/api/sonar_queries.py`  
**Client Access:** `client.sonar_queries`

---

### Users
```
GET    /api/3/users                     - List all users
POST   /api/3/users                     - Create user
GET    /api/3/users/{id}                - Get specific user
PUT    /api/3/users/{id}                - Update user
DELETE /api/3/users/{id}                - Delete user
```

**Module:** `src/rapid7/api/users.py`  
**Client Access:** `client.users`

---

## Common Query Parameters

### Pagination
```python
page: int = 0        # Zero-based page index
size: int = 500      # Number of results per page (max 500)
```

### Sorting
```python
sort: List[str]      # Sort criteria: ["property,ASC|DESC"]
                     # Example: ["name,ASC", "id,DESC"]
```

### Filtering
```python
filters: Dict[str, Any]  # Filter parameters (endpoint-specific)
```

---

## Response Structure

All paginated endpoints return responses in this structure:

```json
{
  "page": {
    "number": 0,
    "size": 500,
    "totalPages": 10,
    "totalResources": 4523
  },
  "resources": [
    {
      "id": 123,
      "...": "resource data"
    }
  ],
  "links": [
    {
      "href": "https://console:3780/api/3/...",
      "rel": "self"
    }
  ]
}
```

---

## Authentication

All endpoints require HTTP Basic Authentication:

```python
from rapid7 import InsightVMClient

# Credentials from environment variables
client = InsightVMClient()

# Or explicit credentials
client = InsightVMClient(
    username="admin",
    password="password",
    base_url="https://console.example.com:3780"
)
```

Required environment variables:
- `INSIGHTVM_API_USERNAME`
- `INSIGHTVM_API_PASSWORD`
- `INSIGHTVM_BASE_URL`

---

## Usage Examples

### List Assets
```python
from rapid7 import InsightVMClient

client = InsightVMClient()
assets = client.assets.list(page=0, size=100)

for asset in assets['resources']:
    print(f"{asset['id']}: {asset['ip']}")
```

### Start Site Scan
```python
scan = client.scans.start_site_scan(
    site_id=123,
    scan_name="Security Audit",
    scan_template_id="full-audit-without-web-spider"
)
print(f"Scan started: {scan['id']}")
```

### Generate Report
```python
# Start generation
instance_id = client.reports.generate(report_id=42)

# Wait for completion
instance = client.reports.wait_for_completion(42, instance_id)

# Download report
content = client.reports.download(42, instance_id)
with open('report.pdf', 'wb') as f:
    f.write(content)
```

---

## References

- **Official API Documentation:** https://docs.rapid7.com/insightvm/restful-api/
- **API Specification:** https://help.rapid7.com/insightvm/en-us/api/index.html
- **Context7 Documentation:** https://github.com/riza/rapid7-insightvm-api-docs
- **Library Documentation:** [docs/API_REFERENCE.md](./API_REFERENCE.md)

---

## Notes

1. All endpoints use the `/api/3/` prefix (API version 3)
2. Multi-word endpoints use underscores: `scan_engines`, `asset_groups`
3. Maximum page size is 500 for pagination
4. SSL verification can be disabled for self-signed certificates
5. All timestamps are in ISO 8601 format
6. HTTP status codes follow REST conventions (200, 201, 204, 400, 401, 403, 404, 500)

---

**For detailed implementation examples and API usage, see:**
- [API_REFERENCE.md](./API_REFERENCE.md) - Complete API documentation
- [EXAMPLES.md](./EXAMPLES.md) - Practical code examples
- [API_REVIEW_FINDINGS.md](./API_REVIEW_FINDINGS.md) - Implementation review
