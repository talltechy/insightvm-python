# Site Management API Documentation

## Overview

The Site Management functionality in InsightVM-Python v2.0 has been **standardized** to follow consistent patterns across all API modules. This standardization separates core CRUD operations from advanced utility functions.

### Architecture

**Two-Component Design:**

1. **`SiteAPI`** (Core) - `src/rapid7/api/sites.py`
   - Standard CRUD operations (list, get, create, update, delete)
   - Resource access methods (assets, scan engines, templates, scans)
   - Follows BaseAPI inheritance pattern
   - Accessed via: `client.sites`

2. **`SiteManagementTools`** (Utilities) - `src/rapid7/tools/site_management.py`
   - Advanced bulk operations
   - Pattern-based filtering
   - Mass delete operations with safety features
   - Helper methods for common workflows
   - Standalone utility class

**Why This Design?**
- **Consistency**: Matches patterns in scan_engines, scan_templates, and other modules
- **Separation of Concerns**: Core API vs. utility helpers
- **Maintainability**: Easier to extend and test
- **Clarity**: Clear distinction between standard operations and advanced workflows

---

## Part 1: Core SiteAPI (Standard Operations)

### Quick Start

```python
from rapid7 import InsightVMClient

# Create client
client = InsightVMClient()

# List all sites with pagination
sites_page = client.sites.list(page=0, size=100)
print(f"Found {sites_page['page']['totalResources']} total sites")

# Get specific site details
site = client.sites.get_site(site_id=123)
print(f"Site: {site['name']}")

# Create new site
new_site = client.sites.create({
    "name": "Production Servers",
    "description": "All production infrastructure",
    "scanEngineId": 3,
    "scanTemplateId": "full-audit-without-web-spider"
})

# Update existing site
updated_site = client.sites.update(site_id=123, site_data={
    "name": "Production Servers - Updated",
    "description": "Updated description"
})

# Delete a site
client.sites.delete_site(site_id=456)
```

### Standard CRUD Operations

#### `list(page=0, size=10, sort=None)`
List sites with pagination.

**Parameters:**
- `page` (int): Page number (default: 0)
- `size` (int): Results per page (default: 10, max: 500)
- `sort` (list): Sort criteria (e.g., `['id,asc']`)

**Returns:** Dictionary with paginated site list

```python
# Get first page
sites = client.sites.list(page=0, size=100)

# Get second page
sites_page2 = client.sites.list(page=1, size=100)

# With sorting
sites_sorted = client.sites.list(sort=['name,asc'])
```

#### `get_site(site_id)`
Get details for a specific site.

**Parameters:**
- `site_id` (int): Site ID

**Returns:** Dictionary with site details

```python
site = client.sites.get_site(site_id=123)
print(f"Name: {site['name']}")
print(f"Description: {site['description']}")
print(f"Scan Engine: {site.get('scanEngineId')}")
print(f"Scan Template: {site.get('scanTemplateId')}")
```

#### `create(site_config)`
Create a new site.

**Parameters:**
- `site_config` (dict): Site configuration

**Returns:** Dictionary with created site details

**Required Fields:**
- `name` (str): Site name

**Optional Fields:**
- `description` (str): Site description
- `scanEngineId` (int): Scan engine ID
- `scanTemplateId` (str): Scan template ID
- `included` (dict): Included scan targets
- `excluded` (dict): Excluded scan targets

```python
# Minimal site
new_site = client.sites.create({
    "name": "Test Site"
})

# Complete site configuration
new_site = client.sites.create({
    "name": "Corporate Network",
    "description": "Main corporate network",
    "scanEngineId": 3,
    "scanTemplateId": "full-audit-without-web-spider",
    "included": {
        "addresses": ["192.168.1.0/24", "10.0.0.1-10.0.0.50"]
    },
    "excluded": {
        "addresses": ["192.168.1.1"]  # Exclude gateway
    }
})
```

#### `update(site_id, site_data)`
Update an existing site.

**Parameters:**
- `site_id` (int): Site ID
- `site_data` (dict): Updated site configuration

**Returns:** Dictionary with updated site details

```python
# Update site name and description
updated = client.sites.update(
    site_id=123,
    site_data={
        "name": "Corporate Network - Renamed",
        "description": "Updated description"
    }
})

# Update scan configuration
updated = client.sites.update(
    site_id=123,
    site_data={
        "scanEngineId": 5,
        "scanTemplateId": "discovery"
    }
})
```

#### `delete_site(site_id)`
Delete a site.

**Parameters:**
- `site_id` (int): Site ID

**Returns:** None

```python
# Delete a site
client.sites.delete_site(site_id=456)
```

**⚠️ Note:** Method renamed from `delete()` to `delete_site()` to avoid conflicts with BaseAPI.

### Resource Access Methods

#### `get_assets(site_id, page=0, size=10)`
Get assets in a site.

**Parameters:**
- `site_id` (int): Site ID
- `page` (int): Page number
- `size` (int): Results per page

**Returns:** Dictionary with paginated asset list

```python
# Get first page of assets
assets = client.sites.get_assets(site_id=123, page=0, size=100)
print(f"Total assets: {assets['page']['totalResources']}")

for asset in assets['resources']:
    print(f"- {asset['id']}: {asset['ip']}")
```

#### `get_scan_engine(site_id)`
Get the scan engine assigned to a site.

**Parameters:**
- `site_id` (int): Site ID

**Returns:** Dictionary with scan engine details

```python
engine = client.sites.get_scan_engine(site_id=123)
print(f"Engine: {engine['name']} (ID: {engine['id']})")
print(f"Status: {engine['status']}")
```

#### `set_scan_engine(site_id, engine_id)`
Assign a scan engine to a site.

**Parameters:**
- `site_id` (int): Site ID
- `engine_id` (int): Scan engine ID

**Returns:** None

```python
# Assign scan engine
client.sites.set_scan_engine(site_id=123, engine_id=5)
```

#### `get_scan_template(site_id)`
Get the scan template assigned to a site.

**Parameters:**
- `site_id` (int): Site ID

**Returns:** Dictionary with scan template details

```python
template = client.sites.get_scan_template(site_id=123)
print(f"Template: {template['name']} (ID: {template['id']})")
print(f"Description: {template['description']}")
```

#### `set_scan_template(site_id, template_id)`
Assign a scan template to a site.

**Parameters:**
- `site_id` (int): Site ID
- `template_id` (str): Scan template ID

**Returns:** None

```python
# Assign scan template
client.sites.set_scan_template(
    site_id=123,
    template_id="full-audit-without-web-spider"
)
```

#### `get_scans(site_id, active=None, page=0, size=10)`
Get scans for a site.

**Parameters:**
- `site_id` (int): Site ID
- `active` (bool, optional): Filter by active status
- `page` (int): Page number
- `size` (int): Results per page

**Returns:** Dictionary with paginated scan list

```python
# Get all scans
scans = client.sites.get_scans(site_id=123)

# Get only active scans
active_scans = client.sites.get_scans(site_id=123, active=True)

# Get completed scans
completed_scans = client.sites.get_scans(site_id=123, active=False)
```

#### `start_scan(site_id, scan_name=None, hosts=None)`
Start an ad-hoc scan for a site.

**Parameters:**
- `site_id` (int): Site ID
- `scan_name` (str, optional): Custom scan name
- `hosts` (list, optional): Specific hosts to scan

**Returns:** Dictionary with scan details including scan ID

```python
# Start scan for entire site
scan = client.sites.start_scan(site_id=123)
print(f"Started scan: {scan['id']}")

# Start scan with custom name
scan = client.sites.start_scan(
    site_id=123,
    scan_name="Emergency Security Scan"
)

# Start scan for specific hosts
scan = client.sites.start_scan(
    site_id=123,
    hosts=["192.168.1.10", "192.168.1.20"]
)
```

### Scan Target Configuration

#### `get_included_targets(site_id)`
Get included scan targets for a site.

**Parameters:**
- `site_id` (int): Site ID

**Returns:** Dictionary with included targets

```python
targets = client.sites.get_included_targets(site_id=123)
print(f"Addresses: {targets.get('addresses', [])}")
print(f"Asset Groups: {targets.get('assetGroups', [])}")
```

#### `set_included_targets(site_id, targets)`
Set included scan targets for a site.

**Parameters:**
- `site_id` (int): Site ID
- `targets` (dict): Included targets configuration

**Returns:** None

```python
# Set IP ranges
client.sites.set_included_targets(
    site_id=123,
    targets={
        "addresses": [
            "192.168.1.0/24",
            "10.0.0.1-10.0.0.50"
        ]
    }
)

# Include asset groups
client.sites.set_included_targets(
    site_id=123,
    targets={
        "assetGroups": [45, 67]
    }
)
```

#### `get_excluded_targets(site_id)`
Get excluded scan targets for a site.

**Parameters:**
- `site_id` (int): Site ID

**Returns:** Dictionary with excluded targets

```python
excluded = client.sites.get_excluded_targets(site_id=123)
print(f"Excluded addresses: {excluded.get('addresses', [])}")
```

#### `set_excluded_targets(site_id, targets)`
Set excluded scan targets for a site.

**Parameters:**
- `site_id` (int): Site ID
- `targets` (dict): Excluded targets configuration

**Returns:** None

```python
# Exclude specific IPs (e.g., gateways, firewalls)
client.sites.set_excluded_targets(
    site_id=123,
    targets={
        "addresses": ["192.168.1.1", "192.168.1.254"]
    }
)
```

---

## Part 2: SiteManagementTools (Advanced Operations)

For bulk operations, filtering, and advanced workflows, use the `SiteManagementTools` utility class.

### Quick Start

```python
from rapid7 import InsightVMClient
from rapid7.tools.site_management import SiteManagementTools

# Create client and tools
client = InsightVMClient()
tools = SiteManagementTools(client)

# Get all sites (auto-pagination)
all_sites = tools.get_all_sites()
print(f"Total sites: {len(all_sites)}")

# Filter by name pattern
test_sites = tools.filter_by_name_pattern(
    all_sites,
    starts_with="Test"
)

# Find empty sites
empty_sites = tools.filter_empty_sites(all_sites)
print(f"Empty sites: {len(empty_sites)}")

# Mass delete with dry-run (safe by default)
tools.mass_delete(
    [site['id'] for site in test_sites],
    dry_run=True  # Preview first
)
```

### Initialization

```python
from rapid7 import InsightVMClient
from rapid7.tools.site_management import SiteManagementTools

# Create tools instance
client = InsightVMClient()
tools = SiteManagementTools(client)
```

### Bulk Retrieval

#### `get_all_sites(batch_size=500)`
Retrieve all sites with automatic pagination.

**Parameters:**
- `batch_size` (int): Results per API call (default: 500)

**Returns:** List of all sites

```python
# Get all sites
all_sites = tools.get_all_sites()
print(f"Total sites: {len(all_sites)}")

# Smaller batch size for slower connections
all_sites = tools.get_all_sites(batch_size=100)
```

### Filtering Operations

#### `filter_by_name_pattern(sites, starts_with=None, ends_with=None, contains=None)`
Filter sites by name patterns.

**Parameters:**
- `sites` (list): List of sites to filter
- `starts_with` (str, optional): Name prefix
- `ends_with` (str, optional): Name suffix
- `contains` (str, optional): Substring in name

**Returns:** Filtered list of sites

```python
all_sites = tools.get_all_sites()

# Sites starting with "Test"
test_sites = tools.filter_by_name_pattern(all_sites, starts_with="Test")

# Sites ending with "Prod"
prod_sites = tools.filter_by_name_pattern(all_sites, ends_with="Prod")

# Sites containing "Development"
dev_sites = tools.filter_by_name_pattern(all_sites, contains="Development")

# Multiple criteria (AND logic)
specific_sites = tools.filter_by_name_pattern(
    all_sites,
    starts_with="Test",
    contains="API"
)
```

#### `filter_empty_sites(sites)`
Filter sites that have no assets.

**Parameters:**
- `sites` (list): List of sites to filter

**Returns:** List of sites with no assets

```python
all_sites = tools.get_all_sites()
empty_sites = tools.filter_empty_sites(all_sites)

print(f"Found {len(empty_sites)} empty sites:")
for site in empty_sites:
    print(f"- {site['name']} (ID: {site['id']})")
```

#### `filter_by_ids(sites, site_ids)`
Filter sites by specific IDs.

**Parameters:**
- `sites` (list): List of sites to filter
- `site_ids` (list): List of site IDs to keep

**Returns:** Filtered list of sites

```python
all_sites = tools.get_all_sites()

# Get specific sites
selected_sites = tools.filter_by_ids(
    all_sites,
    site_ids=[123, 456, 789]
)
```

### Bulk Operations

#### `mass_delete(site_ids, dry_run=True, continue_on_error=False)`
Delete multiple sites with safety features.

**Parameters:**
- `site_ids` (list): List of site IDs to delete
- `dry_run` (bool): Preview mode (default: True)
- `continue_on_error` (bool): Continue if errors occur (default: False)

**Returns:** Dictionary with results

**Safety Features:**
- ✅ Dry-run mode by default (preview before execution)
- ✅ Validation before deletion
- ✅ Continue on error option
- ✅ Detailed result reporting

```python
# SAFE: Preview first (dry_run=True by default)
result = tools.mass_delete([123, 456, 789], dry_run=True)
print(f"Would delete: {result['would_delete']}")
print(f"Would skip: {result['would_skip']}")

# After review, execute for real
result = tools.mass_delete([123, 456, 789], dry_run=False)
print(f"Deleted: {result['deleted']}")
print(f"Failed: {result['failed']}")
print(f"Errors: {result['errors']}")

# Continue even if some deletions fail
result = tools.mass_delete(
    [123, 456, 789],
    dry_run=False,
    continue_on_error=True
)
```

#### `delete_by_pattern(pattern, starts_with=None, ends_with=None, contains=None, dry_run=True)`
Delete sites matching name patterns.

**Parameters:**
- `pattern` (str, optional): Generic pattern (deprecated, use specific parameters)
- `starts_with` (str, optional): Name prefix
- `ends_with` (str, optional): Name suffix
- `contains` (str, optional): Substring in name
- `dry_run` (bool): Preview mode (default: True)

**Returns:** Dictionary with results

```python
# Preview deletion of test sites
result = tools.delete_by_pattern(starts_with="Test", dry_run=True)
print(f"Found {len(result['matched_sites'])} test sites")

# Delete all temporary sites (after review)
result = tools.delete_by_pattern(contains="Temp", dry_run=False)

# Delete sites with specific suffix
result = tools.delete_by_pattern(ends_with="-OLD", dry_run=False)
```

### Utility Methods

#### `get_asset_count(site_id)`
Get the number of assets in a site.

**Parameters:**
- `site_id` (int): Site ID

**Returns:** Integer count of assets

```python
# Get asset count for a site
count = tools.get_asset_count(site_id=123)
print(f"Site has {count} assets")

# Check multiple sites
all_sites = tools.get_all_sites()
for site in all_sites:
    count = tools.get_asset_count(site['id'])
    print(f"{site['name']}: {count} assets")
```

---

## Part 3: Migration Guide (v1.0 → v2.0)

### Breaking Changes

**Sites API has been standardized**, with custom helper methods moved to `SiteManagementTools`.

#### Method Renames

| Old Method | New Method | Location |
|------------|------------|----------|
| `client.sites.get()` | `client.sites.get_site()` | SiteAPI |
| `client.sites.delete()` | `client.sites.delete_site()` | SiteAPI |

#### Moved to SiteManagementTools

| Old Method | New Location |
|------------|--------------|
| `client.sites.get_all_sites()` | `tools.get_all_sites()` |
| `client.sites.filter_by_name_pattern()` | `tools.filter_by_name_pattern()` |
| `client.sites.filter_empty_sites()` | `tools.filter_empty_sites()` |
| `client.sites.filter_by_ids()` | `tools.filter_by_ids()` |
| `client.sites.mass_delete()` | `tools.mass_delete()` |
| `client.sites.delete_by_pattern()` | `tools.delete_by_pattern()` |
| `client.sites.get_asset_count()` | `tools.get_asset_count()` |

### Migration Examples

#### Example 1: Get All Sites

**Before (v1.0):**
```python
from rapid7 import InsightVMClient

client = InsightVMClient()
all_sites = client.sites.get_all_sites()
```

**After (v2.0):**
```python
from rapid7 import InsightVMClient
from rapid7.tools.site_management import SiteManagementTools

client = InsightVMClient()
tools = SiteManagementTools(client)
all_sites = tools.get_all_sites()
```

#### Example 2: Filter and Delete

**Before (v1.0):**
```python
client = InsightVMClient()

# Get and filter
all_sites = client.sites.get_all_sites()
test_sites = client.sites.filter_by_name_pattern(
    all_sites,
    starts_with="Test"
)

# Delete
result = client.sites.mass_delete(
    [site['id'] for site in test_sites],
    dry_run=False
)
```

**After (v2.0):**
```python
from rapid7 import InsightVMClient
from rapid7.tools.site_management import SiteManagementTools

client = InsightVMClient()
tools = SiteManagementTools(client)

# Get and filter
all_sites = tools.get_all_sites()
test_sites = tools.filter_by_name_pattern(
    all_sites,
    starts_with="Test"
)

# Delete
result = tools.mass_delete(
    [site['id'] for site in test_sites],
    dry_run=False
)
```

#### Example 3: Get Site Details

**Before (v1.0):**
```python
client = InsightVMClient()
site = client.sites.get(site_id=123)  # Old method name
```

**After (v2.0):**
```python
client = InsightVMClient()
site = client.sites.get_site(site_id=123)  # Renamed to avoid BaseAPI conflict
```

#### Example 4: Delete Site

**Before (v1.0):**
```python
client = InsightVMClient()
client.sites.delete(site_id=123)  # Old method name
```

**After (v2.0):**
```python
client = InsightVMClient()
client.sites.delete_site(site_id=123)  # Renamed to avoid BaseAPI conflict
```

### Migration Checklist

- [ ] Replace `client.sites.get()` with `client.sites.get_site()`
- [ ] Replace `client.sites.delete()` with `client.sites.delete_site()`
- [ ] Import `SiteManagementTools` for bulk operations
- [ ] Create tools instance: `tools = SiteManagementTools(client)`
- [ ] Update filtering calls to use `tools.filter_*()`
- [ ] Update bulk operations to use `tools.mass_delete()` or `tools.delete_by_pattern()`
- [ ] Update asset count calls to use `tools.get_asset_count()`

---

## Benefits of New Architecture

### Consistency
- Sites API now matches patterns used in scan_engines, scan_templates, scans, and reports modules
- Predictable method names and behaviors across all modules
- Standard CRUD operations follow BaseAPI inheritance

### Separation of Concerns
- **Core API** (`SiteAPI`): Standard operations for day-to-day use
- **Utility Tools** (`SiteManagementTools`): Advanced bulk operations and workflows

### Maintainability
- Easier to extend with new features
- Clear boundaries between core and utility functionality
- Follows industry-standard design patterns

### Safety
- SiteManagementTools maintains all safety features (dry-run mode by default)
- No change to safety mechanisms, just organization

---

## Complete Examples

### Example 1: Site Lifecycle

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Create site
new_site = client.sites.create({
    "name": "Corporate Network",
    "description": "Main corporate infrastructure",
    "scanEngineId": 3,
    "scanTemplateId": "full-audit-without-web-spider",
    "included": {
        "addresses": ["192.168.1.0/24"]
    }
})
site_id = new_site['id']

# Configure scan targets
client.sites.set_included_targets(site_id, {
    "addresses": ["192.168.1.0/24", "10.0.0.0/24"]
})

client.sites.set_excluded_targets(site_id, {
    "addresses": ["192.168.1.1", "10.0.0.1"]  # Exclude gateways
})

# Start scan
scan = client.sites.start_scan(site_id)
print(f"Started scan: {scan['id']}")

# Later: Update site
client.sites.update(site_id, {
    "description": "Updated description"
})

# Eventually: Delete site
client.sites.delete_site(site_id)
```

### Example 2: Bulk Cleanup

```python
from rapid7 import InsightVMClient
from rapid7.tools.site_management import SiteManagementTools

client = InsightVMClient()
tools = SiteManagementTools(client)

# Find sites to clean up
all_sites = tools.get_all_sites()

# Get empty sites
empty_sites = tools.filter_empty_sites(all_sites)
print(f"Found {len(empty_sites)} empty sites")

# Get old test sites
test_sites = tools.filter_by_name_pattern(all_sites, starts_with="Test")
print(f"Found {len(test_sites)} test sites")

# Preview deletion
site_ids_to_delete = [site['id'] for site in empty_sites + test_sites]
preview = tools.mass_delete(site_ids_to_delete, dry_run=True)
print(f"Would delete: {preview['would_delete']}")

# Execute after review
result = tools.mass_delete(site_ids_to_delete, dry_run=False)
print(f"Deleted: {result['deleted']}")
print(f"Failed: {result['failed']}")
```

### Example 3: Site Audit

```python
from rapid7 import InsightVMClient
from rapid7.tools.site_management import SiteManagementTools

client = InsightVMClient()
tools = SiteManagementTools(client)

# Audit all sites
all_sites = tools.get_all_sites()

print(f"Site Audit Report")
print(f"=" * 50)
print(f"Total sites: {len(all_sites)}")

# Check for empty sites
empty_sites = tools.filter_empty_sites(all_sites)
print(f"Empty sites: {len(empty_sites)}")

# Asset distribution
for site in all_sites:
    asset_count = tools.get_asset_count(site['id'])
    scan_engine = client.sites.get_scan_engine(site['id'])
    scan_template = client.sites.get_scan_template(site['id'])
    
    print(f"\nSite: {site['name']} (ID: {site['id']})")
    print(f"  Assets: {asset_count}")
    print(f"  Engine: {scan_engine['name']}")
    print(f"  Template: {scan_template['name']}")
```

---

## Best Practices

### Use Core SiteAPI For
- ✅ Standard CRUD operations (create, read, update, delete)
- ✅ Individual site management
- ✅ Scan configuration
- ✅ Resource access (assets, engines, templates)

### Use SiteManagementTools For
- ✅ Bulk operations across multiple sites
- ✅ Pattern-based filtering
- ✅ Mass deletion operations
- ✅ Auditing and reporting
- ✅ Cleanup workflows

### General Guidelines
- Always use `dry_run=True` first for bulk deletions
- Verify filtering results before bulk operations
- Use auto-pagination (`get_all_sites()`) for complete datasets
- Handle errors gracefully with `continue_on_error` when appropriate
- Review site configurations before applying changes

---

## Error Handling

```python
import requests
from rapid7 import InsightVMClient
from rapid7.tools.site_management import SiteManagementTools

client = InsightVMClient()
tools = SiteManagementTools(client)

try:
    # Get site
    site = client.sites.get_site(site_id=123)
    
    # Update site
    updated = client.sites.update(site_id=123, site_data={
        "name": "New Name"
    })
    
    # Bulk operation
    result = tools.mass_delete([123, 456], dry_run=False)
    
except ValueError as e:
    print(f"Configuration error: {e}")
except requests.exceptions.RequestException as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Additional Resources

- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Scans API](SCANS_API.md) - Scan management
- [Reports API](REPORTS_API.md) - Report generation
- [Migration Guide](../MIGRATION.md) - v1.0 to v2.0 upgrade guide

---

## Summary

**Site Management in v2.0:**
1. **SiteAPI** - Standard operations following BaseAPI patterns
2. **SiteManagementTools** - Advanced bulk operations and utilities
3. **Clear separation** - Core API vs. utility helpers
4. **Consistent design** - Matches other API modules
5. **Migration path** - Simple updates for v1.0 users

The new architecture provides better organization, consistency, and maintainability while preserving all functionality and safety features.
