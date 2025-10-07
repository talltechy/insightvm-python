# API Reference

Complete reference for InsightVM-Python v2.0 API.

## Table of Contents

- [InsightVMClient](#insightvmclient)
- [Authentication](#authentication)
- [AssetAPI](#assetapi)
- [AssetGroupAPI](#assetgroupapi)
- [BaseAPI](#baseapi)
- [Error Handling](#error-handling)

---

## InsightVMClient

The main entry point for all InsightVM operations.

### Constructor

```python
InsightVMClient(
    username: Optional[str] = None,
    password: Optional[str] = None,
    base_url: Optional[str] = None,
    verify_ssl: Optional[bool] = None,
    timeout: Tuple[int, int] = (10, 90)
)
```

**Parameters:**
- `username` (str, optional): InsightVM username. Defaults to `INSIGHTVM_API_USERNAME` env variable.
- `password` (str, optional): InsightVM password. Defaults to `INSIGHTVM_API_PASSWORD` env variable.
- `base_url` (str, optional): InsightVM console URL. Defaults to `INSIGHTVM_BASE_URL` env variable.
- `verify_ssl` (bool, optional): Enable SSL verification. Defaults to `INSIGHTVM_VERIFY_SSL` env variable or `True`.
- `timeout` (tuple, optional): Connection and read timeouts in seconds. Default is `(10, 90)`.

**Raises:**
- `ValueError`: If required credentials are missing.

**Example:**
```python
from rapid7 import InsightVMClient

# Using environment variables
client = InsightVMClient()

# Explicit configuration
client = InsightVMClient(
    username="admin",
    password="password123",
    base_url="https://console:3780",
    verify_ssl=False,
    timeout=(10, 90)
)
```

### Properties

#### client.assets

Returns an `AssetAPI` instance for asset operations.

**Type:** `AssetAPI`

**Example:**
```python
assets = client.assets.list()
```

#### client.asset_groups

Returns an `AssetGroupAPI` instance for asset group operations.

**Type:** `AssetGroupAPI`

**Example:**
```python
groups = client.asset_groups.list()
```

### Context Manager Support

The client can be used as a context manager for automatic cleanup.

```python
with InsightVMClient() as client:
    assets = client.assets.list()
    # Client automatically cleaned up
```

### Factory Function

#### create_client()

Convenience factory function to create an InsightVMClient.

```python
from rapid7 import create_client

client = create_client()
```

---

## Authentication

### InsightVMAuth

Handles authentication for InsightVM API.

```python
from rapid7.auth import InsightVMAuth

auth = InsightVMAuth(
    username: Optional[str] = None,
    password: Optional[str] = None,
    base_url: Optional[str] = None
)
```

**Parameters:**
- `username` (str, optional): API username
- `password` (str, optional): API password
- `base_url` (str, optional): Console base URL

**Properties:**
- `auth`: Returns `requests.auth.HTTPBasicAuth` object
- `username`: The configured username
- `password`: The configured password (read-only)
- `base_url`: The configured base URL

**Example:**
```python
from rapid7.auth import InsightVMAuth
import requests

auth = InsightVMAuth()
response = requests.get(
    f"{auth.base_url}/api/3/assets",
    auth=auth.auth
)
```

### PlatformAuth

Handles authentication for Rapid7 Platform API.

```python
from rapid7.auth import PlatformAuth

auth = PlatformAuth(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
)
```

**Parameters:**
- `api_key` (str, optional): Platform API key
- `base_url` (str, optional): Platform base URL

**Methods:**
- `get_headers()`: Returns dict with API key header

---

## AssetAPI

Comprehensive asset management operations.

### list()

List assets with pagination.

```python
client.assets.list(
    page: int = 0,
    size: int = 500,
    sort: Optional[List[str]] = None,
    filters: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `page` (int): Page number (0-indexed)
- `size` (int): Number of assets per page (max 500)
- `sort` (list, optional): Sort criteria
- `filters` (dict, optional): Filter criteria

**Returns:** Dict with `resources` (list of assets) and pagination info

**Example:**
```python
# Get first page
assets = client.assets.list(page=0, size=100)

# With sorting
assets = client.assets.list(
    page=0,
    size=100,
    sort=["riskScore,DESC"]
)
```

### get_asset()

Get details for a specific asset.

```python
client.assets.get_asset(asset_id: int) -> Dict[str, Any]
```

**Parameters:**
- `asset_id` (int): The asset identifier

**Returns:** Dict with asset details

**Example:**
```python
asset = client.assets.get_asset(123)
print(f"Hostname: {asset['hostname']}")
print(f"IP: {asset['ip']}")
print(f"Risk Score: {asset['riskScore']}")
```

### search()

Search for assets using advanced criteria.

```python
client.assets.search(
    criteria: Dict[str, Any],
    page: int = 0,
    size: int = 500
) -> Dict[str, Any]
```

**Parameters:**
- `criteria` (dict): Search criteria with filters and match type
- `page` (int): Page number
- `size` (int): Results per page

**Returns:** Dict with matching assets

**Example:**
```python
# Search for high-risk Windows servers
results = client.assets.search({
    "filters": [
        {
            "field": "risk-score",
            "operator": "is-greater-than",
            "value": 20000
        },
        {
            "field": "operating-system",
            "operator": "contains",
            "value": "Windows Server"
        }
    ],
    "match": "all"
})
```

**Available operators:**
- `is`, `is-not`
- `contains`, `does-not-contain`
- `starts-with`, `ends-with`
- `is-greater-than`, `is-less-than`
- `is-between`, `is-not-between`
- `in`, `not-in`

### get_all()

Get all assets with automatic pagination.

```python
client.assets.get_all(batch_size: int = 500) -> List[Dict[str, Any]]
```

**Parameters:**
- `batch_size` (int): Number of assets per API call

**Returns:** List of all assets

**Example:**
```python
# Get all assets (handles pagination automatically)
all_assets = client.assets.get_all()
print(f"Total assets: {len(all_assets)}")
```

### get_vulnerabilities()

Get vulnerabilities for a specific asset.

```python
client.assets.get_vulnerabilities(asset_id: int) -> Dict[str, Any]
```

**Parameters:**
- `asset_id` (int): The asset identifier

**Returns:** Dict with vulnerability data

**Example:**
```python
vulns = client.assets.get_vulnerabilities(123)
print(f"Critical vulnerabilities: {vulns['critical']}")
```

### get_software()

Get software inventory for an asset.

```python
client.assets.get_software(asset_id: int) -> Dict[str, Any]
```

**Parameters:**
- `asset_id` (int): The asset identifier

**Returns:** Dict with software inventory

### get_services()

Get running services on an asset.

```python
client.assets.get_services(asset_id: int) -> Dict[str, Any]
```

**Parameters:**
- `asset_id` (int): The asset identifier

**Returns:** Dict with service information

### get_tags()

Get tags associated with an asset.

```python
client.assets.get_tags(asset_id: int) -> Dict[str, Any]
```

**Parameters:**
- `asset_id` (int): The asset identifier

**Returns:** Dict with tag list

### add_tag()

Add a tag to an asset.

```python
client.assets.add_tag(asset_id: int, tag_id: int) -> Dict[str, Any]
```

**Parameters:**
- `asset_id` (int): The asset identifier
- `tag_id` (int): The tag identifier

**Returns:** Success response

### remove_tag()

Remove a tag from an asset.

```python
client.assets.remove_tag(asset_id: int, tag_id: int) -> Dict[str, Any]
```

**Parameters:**
- `asset_id` (int): The asset identifier
- `tag_id` (int): The tag identifier

**Returns:** Success response

---

## AssetGroupAPI

Asset group management operations.

### list()

List all asset groups.

```python
client.asset_groups.list() -> Dict[str, Any]
```

**Returns:** Dict with asset groups list

**Example:**
```python
groups = client.asset_groups.list()
for group in groups['resources']:
    print(f"{group['name']}: {group['assets']} assets")
```

### get_group()

Get details for a specific asset group.

```python
client.asset_groups.get_group(group_id: int) -> Dict[str, Any]
```

**Parameters:**
- `group_id` (int): The asset group identifier

**Returns:** Dict with group details

### create()

Create a new asset group.

```python
client.asset_groups.create(
    name: str,
    description: str,
    search_criteria: Dict[str, Any],
    group_type: str = 'dynamic'
) -> Dict[str, Any]
```

**Parameters:**
- `name` (str): Group name
- `description` (str): Group description
- `search_criteria` (dict): Criteria for dynamic groups
- `group_type` (str): Either 'dynamic' or 'static'

**Returns:** Dict with created group details

**Example:**
```python
group = client.asset_groups.create(
    name="Critical Servers",
    description="All servers with critical vulnerabilities",
    search_criteria={
        "filters": [
            {
                "field": "cvss-score",
                "operator": "is-greater-than",
                "value": 9.0
            }
        ],
        "match": "all"
    }
)
```

### create_high_risk()

Convenience method to create a high-risk asset group.

```python
client.asset_groups.create_high_risk(
    name: str = "High Risk Assets",
    description: str = "Assets with risk score above threshold",
    threshold: int = 25000
) -> Dict[str, Any]
```

**Parameters:**
- `name` (str): Group name
- `description` (str): Group description
- `threshold` (int): Minimum risk score

**Returns:** Dict with created group

**Example:**
```python
group = client.asset_groups.create_high_risk(
    name="Critical Assets",
    threshold=30000
)
```

### update()

Update an existing asset group.

```python
client.asset_groups.update(
    group_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    search_criteria: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `group_id` (int): The asset group identifier
- `name` (str, optional): New name
- `description` (str, optional): New description
- `search_criteria` (dict, optional): New search criteria

**Returns:** Dict with updated group

### delete_group()

Delete an asset group.

```python
client.asset_groups.delete_group(group_id: int) -> Dict[str, Any]
```

**Parameters:**
- `group_id` (int): The asset group identifier

**Returns:** Success response

### get_assets()

Get assets that belong to a group.

```python
client.asset_groups.get_assets(group_id: int) -> Dict[str, Any]
```

**Parameters:**
- `group_id` (int): The asset group identifier

**Returns:** Dict with asset list

### add_asset()

Add an asset to a static group.

```python
client.asset_groups.add_asset(
    group_id: int,
    asset_id: int
) -> Dict[str, Any]
```

**Parameters:**
- `group_id` (int): The asset group identifier
- `asset_id` (int): The asset identifier

**Returns:** Success response

### remove_asset()

Remove an asset from a static group.

```python
client.asset_groups.remove_asset(
    group_id: int,
    asset_id: int
) -> Dict[str, Any]
```

**Parameters:**
- `group_id` (int): The asset group identifier
- `asset_id` (int): The asset identifier

**Returns:** Success response

### search()

Search for asset groups.

```python
client.asset_groups.search(
    query: str
) -> Dict[str, Any]
```

**Parameters:**
- `query` (str): Search query

**Returns:** Dict with matching groups

---

## BaseAPI

Base class for all API modules. Used internally but can be extended for custom modules.

### Constructor

```python
BaseAPI(
    auth: InsightVMAuth,
    verify_ssl: Optional[bool] = None,
    timeout: Tuple[int, int] = (10, 90)
)
```

### Protected Methods

#### _request()

Make an HTTP request.

```python
_request(
    method: str,
    endpoint: str,
    params: Optional[Dict] = None,
    json: Optional[Dict] = None,
    headers: Optional[Dict] = None
) -> requests.Response
```

#### _build_url()

Construct full API URL.

```python
_build_url(endpoint: str) -> str
```

#### _handle_response()

Process API response.

```python
_handle_response(response: requests.Response) -> Dict[str, Any]
```

---

## Error Handling

### Common Exceptions

#### ValueError

Raised for configuration errors.

```python
try:
    client = InsightVMClient()
except ValueError as e:
    print(f"Configuration error: {e}")
    # Check .env file
```

#### requests.exceptions.RequestException

Base class for all requests errors.

```python
import requests

try:
    assets = client.assets.list()
except requests.exceptions.RequestException as e:
    print(f"API error: {e}")
```

#### requests.exceptions.HTTPError

Raised for HTTP error status codes.

```python
try:
    asset = client.assets.get_asset(99999)
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Asset not found")
    elif e.response.status_code == 401:
        print("Authentication failed")
```

### HTTP Status Codes

- `200-299`: Success
- `400`: Bad Request - Invalid parameters
- `401`: Unauthorized - Invalid credentials
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource doesn't exist
- `429`: Too Many Requests - Rate limit exceeded
- `500+`: Server Error - InsightVM API issue

### Error Response Format

API errors typically include:

```json
{
    "status": 400,
    "message": "Error description",
    "links": []
}
```

### Best Practices

```python
import requests
from rapid7 import InsightVMClient

def safe_api_call():
    try:
        client = InsightVMClient()
        assets = client.assets.get_all()
        return assets
        
    except ValueError as e:
        # Configuration error
        print(f"Config error: {e}")
        print("Check your .env file")
        return None
        
    except requests.exceptions.HTTPError as e:
        # HTTP error
        status = e.response.status_code
        if status == 401:
            print("Authentication failed - check credentials")
        elif status == 404:
            print("Resource not found")
        elif status == 429:
            print("Rate limit exceeded - retry later")
        else:
            print(f"HTTP error {status}: {e}")
        return None
        
    except requests.exceptions.ConnectionError as e:
        # Network error
        print(f"Connection error: {e}")
        print("Check network connectivity and base URL")
        return None
        
    except requests.exceptions.Timeout as e:
        # Timeout error
        print(f"Request timeout: {e}")
        print("Consider increasing timeout values")
        return None
        
    except Exception as e:
        # Unexpected error
        print(f"Unexpected error: {e}")
        return None
```

---

## Type Hints

All functions include comprehensive type hints:

```python
from typing import Dict, List, Any, Optional, Tuple

def list(
    self,
    page: int = 0,
    size: int = 500,
    sort: Optional[List[str]] = None
) -> Dict[str, Any]:
    ...
```

Use a type checker like `mypy` for static type checking:

```bash
pip install mypy
mypy your_script.py
```

---

## See Also

- [Usage Examples](EXAMPLES.md) - Practical code examples
- [Migration Guide](../MIGRATION.md) - Upgrading from v1.0
- [Contributing](../CONTRIBUTING.md) - Development guidelines
