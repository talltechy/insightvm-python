# Migration Guide: v1.0 → v2.0

This guide will help you migrate your code from InsightVM-Python v1.0 to v2.0.

## ⚠️ Breaking Changes

Version 2.0 introduces significant architectural improvements but requires code changes. The good news: the new API is cleaner, more intuitive, and follows industry standards.

## Quick Reference

| Area | v1.0 | v2.0 |
|------|------|------|
| **Authentication** | Manual Base64 | HTTPBasicAuth |
| **Client** | Direct API calls | Unified `InsightVMClient` |
| **Import Path** | `src.rapid7.*` | `rapid7.*` |
| **Environment Variables** | `ivm_host`, `ivm_port` | `INSIGHTVM_BASE_URL` |
| **SSL Config** | Not configurable | `INSIGHTVM_VERIFY_SSL` |

## Step-by-Step Migration

### 1. Update Environment Variables

**v1.0 `.env` format:**
```bash
ivm_host=192.168.10.190
ivm_port=3780
ivm_username=myuser
ivm_password=mypass
```

**v2.0 `.env` format:**
```bash
INSIGHTVM_API_USERNAME=myuser
INSIGHTVM_API_PASSWORD=mypass
INSIGHTVM_BASE_URL=https://192.168.10.190:3780
INSIGHTVM_VERIFY_SSL=false  # if using self-signed certificates
```

**Migration script for .env:**
```bash
# Combine host and port into base URL
# Add INSIGHTVM_ prefix to all variables
# Add VERIFY_SSL configuration
```

### 2. Update Authentication Code

**v1.0 - Manual authentication:**
```python
from src.rapid7.api_r7_auth import get_isvm_basic_auth_header
from src.rapid7.api_r7_api import R7_ISVM_Api

# Get auth header manually
auth_header = get_isvm_basic_auth_header()

# Create API instance
api = R7_ISVM_Api(auth_header, fqdn, "assets", timeout=(10, 90))
```

**v2.0 - Unified client:**
```python
from rapid7 import InsightVMClient

# Authentication handled automatically
client = InsightVMClient()

# Or with explicit configuration
client = InsightVMClient(
    username="myuser",
    password="mypass",
    base_url="https://console:3780",
    verify_ssl=False,
    timeout=(10, 90)
)
```

### 3. Update Import Statements

**v1.0 imports:**
```python
from src.rapid7.api_r7_auth import load_r7_isvm_api_credentials
from src.rapid7.api_r7_auth import get_isvm_basic_auth_header
from src.rapid7.api_r7_api import R7_ISVM_Api
from src.rapid7.api_r7_isvm import get_assets_isvm
from src.rapid7.api_r7_asset_group import create_asset_group
```

**v2.0 imports:**
```python
from rapid7 import InsightVMClient
from rapid7.auth import InsightVMAuth  # if needed separately

# That's it! Everything accessible through client
```

### 4. Migrate Asset Operations

**v1.0 - Function-based:**
```python
from src.rapid7.api_r7_isvm import get_assets_isvm, search_asset_isvm

# Get assets
auth = get_isvm_basic_auth_header()
assets = get_assets_isvm(auth, fqdn, page=0, size=500)

# Search assets
criteria = {"filters": [...], "match": "all"}
results = search_asset_isvm(auth, fqdn, criteria)
```

**v2.0 - Client methods:**
```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Get assets (same parameters)
assets = client.assets.list(page=0, size=500)

# Search assets
criteria = {"filters": [...], "match": "all"}
results = client.assets.search(criteria)

# NEW: Auto-pagination
all_assets = client.assets.get_all(batch_size=500)
```

### 5. Migrate Asset Group Operations

**v1.0 - Function-based:**
```python
from src.rapid7.api_r7_asset_group import create_asset_group

auth = get_isvm_basic_auth_header()
group = create_asset_group(
    auth, 
    fqdn, 
    name="High Risk",
    description="Critical assets",
    search_criteria=criteria
)
```

**v2.0 - Client methods:**
```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Create asset group
group = client.asset_groups.create(
    name="High Risk",
    description="Critical assets",
    search_criteria=criteria
)

# NEW: Convenience method for high-risk groups
group = client.asset_groups.create_high_risk(
    name="High Risk Assets",
    threshold=25000
)

# NEW: Update, delete, manage members
client.asset_groups.update(group_id, name="Updated Name", ...)
client.asset_groups.delete_group(group_id)
client.asset_groups.add_asset(group_id, asset_id)
```

### 6. Update Error Handling

**v1.0:**
```python
try:
    auth = get_isvm_basic_auth_header()
except Exception as e:
    print(f"Auth failed: {e}")
```

**v2.0:**
```python
import requests

try:
    client = InsightVMClient()
    assets = client.assets.list()
except ValueError as e:
    # Configuration error (missing credentials)
    print(f"Config error: {e}")
except requests.exceptions.RequestException as e:
    # API error
    print(f"API error: {e}")
```

### 7. Update Context Management

**v1.0 - Manual cleanup:**
```python
api = R7_ISVM_Api(...)
try:
    result = api._call(...)
finally:
    # Manual cleanup if needed
    pass
```

**v2.0 - Context manager:**
```python
# Automatic cleanup
with InsightVMClient() as client:
    assets = client.assets.list()
    # Client automatically cleaned up
```

## Common Migration Patterns

### Pattern 1: Simple Asset Retrieval

```python
# v1.0
from src.rapid7.api_r7_isvm import get_assets_isvm
auth = get_isvm_basic_auth_header()
assets = get_assets_isvm(auth, fqdn, page=0, size=500)

# v2.0
from rapid7 import InsightVMClient
client = InsightVMClient()
assets = client.assets.list(page=0, size=500)
```

### Pattern 2: Asset Group Creation

```python
# v1.0
from src.rapid7.api_r7_asset_group import create_asset_group
auth = get_isvm_basic_auth_header()
group = create_asset_group(auth, fqdn, "name", "desc", criteria)

# v2.0
from rapid7 import InsightVMClient
client = InsightVMClient()
group = client.asset_groups.create("name", "desc", criteria)
```

### Pattern 3: Bulk Operations

```python
# v1.0 - Manual pagination
all_assets = []
page = 0
while True:
    assets = get_assets_isvm(auth, fqdn, page=page, size=500)
    if not assets['resources']:
        break
    all_assets.extend(assets['resources'])
    page += 1

# v2.0 - Auto-pagination
all_assets = client.assets.get_all(batch_size=500)
```

## New Features in v2.0

Take advantage of these new capabilities:

### 1. Tag Management
```python
# Get asset tags
tags = client.assets.get_tags(asset_id)

# Add tag
client.assets.add_tag(asset_id, tag_id)

# Remove tag
client.assets.remove_tag(asset_id, tag_id)
```

### 2. Enhanced Asset Information
```python
# Get vulnerabilities
vulns = client.assets.get_vulnerabilities(asset_id)

# Get software
software = client.assets.get_software(asset_id)

# Get services
services = client.assets.get_services(asset_id)
```

### 3. Asset Group Management
```python
# List all groups
groups = client.asset_groups.list()

# Get group details
group = client.asset_groups.get_group(group_id)

# Get group members
assets = client.asset_groups.get_assets(group_id)

# Update group
client.asset_groups.update(group_id, name="New Name")

# Delete group
client.asset_groups.delete_group(group_id)
```

## Troubleshooting

### Issue: Import errors

**Problem:** `ModuleNotFoundError: No module named 'src.rapid7'`

**Solution:** Update imports from `src.rapid7.*` to `rapid7.*`

### Issue: Authentication fails

**Problem:** `ValueError: Missing required credentials`

**Solution:** 
1. Check `.env` file exists
2. Verify variable names use `INSIGHTVM_*` prefix
3. Ensure `INSIGHTVM_BASE_URL` includes `https://` and port

### Issue: SSL certificate errors

**Problem:** `SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]`

**Solution:** Add to `.env`:
```bash
INSIGHTVM_VERIFY_SSL=false
```

### Issue: Old files still present

**Problem:** Import errors with both old and new code

**Solution:** The v2.0 codebase has removed old files. If you have a mixed environment:
1. Pull latest code
2. Remove old imports
3. Update to new patterns

## Testing Your Migration

After migrating, test with this script:

```python
from rapid7 import InsightVMClient

def test_migration():
    """Test v2.0 migration"""
    try:
        # Create client
        client = InsightVMClient()
        print("✅ Client created successfully")
        
        # Test asset retrieval
        assets = client.assets.list(page=0, size=10)
        print(f"✅ Retrieved {len(assets.get('resources', []))} assets")
        
        # Test asset groups
        groups = client.asset_groups.list()
        print(f"✅ Retrieved {len(groups.get('resources', []))} asset groups")
        
        print("\n🎉 Migration successful!")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Check your .env file")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_migration()
```

## Getting Help

If you encounter issues during migration:

1. Check this migration guide
2. Review the [API Reference](docs/API_REFERENCE.md)
3. See [examples](docs/EXAMPLES.md) for working code
4. Open an issue on GitHub with:
   - Your v1.0 code
   - Error messages
   - Environment details

## Summary

v2.0 provides a cleaner, more maintainable codebase with:
- ✅ Industry-standard HTTPBasicAuth
- ✅ Intuitive unified client
- ✅ Better error handling
- ✅ More features (auto-pagination, tag management)
- ✅ Type safety with full type hints
- ✅ Context manager support

The migration effort is worth it for the improved developer experience!
