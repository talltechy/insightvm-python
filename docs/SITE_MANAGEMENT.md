# Site Management Guide

This guide covers the Site Management module implemented in InsightVM-Python v2.0.

## Overview

The Site Management module (`SiteAPI`) provides comprehensive operations for managing sites in InsightVM, including:

- Full CRUD operations (Create, Read, Update, Delete)
- Smart filtering by name patterns
- Filter by site IDs
- Filter empty sites (sites with no assets)
- Mass delete operations with dry-run mode
- Site asset information
- Scan engine and template management

## Quick Start

```python
from rapid7 import InsightVMClient

# Initialize client
client = InsightVMClient()

# Access site operations
sites = client.sites
```

## Basic Operations

### List Sites

```python
# List sites with pagination
response = client.sites.list(page=0, size=100)
for site in response['resources']:
    print(f"Site {site['id']}: {site['name']}")

# Get all sites (auto-pagination)
all_sites = client.sites.get_all()
print(f"Total sites: {len(all_sites)}")
```

### Get Site Details

```python
# Get a specific site by ID
site = client.sites.get_site(123)
print(f"Site: {site['name']}")
print(f"Description: {site.get('description', 'N/A')}")
print(f"Type: {site.get('type', 'N/A')}")
```

### Create Site

```python
# Create a new site
new_site = client.sites.create(
    name="Production Servers",
    description="Critical production infrastructure",
    importance="high"
)
print(f"Created site ID: {new_site['id']}")
```

### Update Site

```python
# Update site properties
updated_site = client.sites.update(
    site_id=123,
    name="Updated Site Name",
    importance="high",
    description="Updated description"
)
```

### Delete Site

```python
# Delete a single site
client.sites.delete_site(123)
```

## Smart Filtering

### Filter by Name Pattern

```python
# Get sites starting with 'sn_'
sn_sites = client.sites.filter_by_name_pattern(starts_with='sn_')
print(f"Found {len(sn_sites)} sites starting with 'sn_'")

# Get sites ending with '_prod'
prod_sites = client.sites.filter_by_name_pattern(ends_with='_prod')

# Get sites containing 'test'
test_sites = client.sites.filter_by_name_pattern(contains='test')

# Case-sensitive filtering
exact_sites = client.sites.filter_by_name_pattern(
    starts_with='PROD',
    case_sensitive=True
)
```

### Filter by Site IDs

```python
# Get specific sites by ID
selected_sites = client.sites.filter_by_ids([1, 5, 10, 15, 20])
for site in selected_sites:
    print(f"{site['id']}: {site['name']}")
```

### Filter Empty Sites

```python
# Find sites with no assets
empty_sites = client.sites.filter_empty_sites()
print(f"Found {len(empty_sites)} empty sites")

for site in empty_sites:
    print(f"Empty site: {site['name']} (ID: {site['id']})")
```

### Combined Filtering

```python
# Combine multiple filters
filtered = client.sites.filter_sites(
    name_pattern='sn_',
    empty_only=True
)
print(f"Found {len(filtered)} empty sites starting with 'sn_'")
```

## Site Assets

### Get Site Assets

```python
# Get assets for a site
assets = client.sites.get_assets(site_id=123, page=0, size=100)
for asset in assets['resources']:
    print(f"Asset: {asset['ip']} - {asset.get('hostName', 'N/A')}")

# Get asset count
count = client.sites.get_asset_count(site_id=123)
print(f"Site has {count} assets")
```

## Mass Operations

### Mass Delete with Preview (Dry Run)

```python
# Preview what would be deleted (safe - doesn't delete anything)
preview = client.sites.mass_delete(
    site_ids=[1, 2, 3, 4, 5],
    dry_run=True  # Default is True for safety
)

print(f"Would delete {len(preview['preview'])} sites:")
for site_info in preview['preview']:
    print(f"  - {site_info['name']} (ID: {site_info['id']}, "
          f"Assets: {site_info['asset_count']})")
```

### Mass Delete (Actual Deletion)

```python
# Actually delete sites
result = client.sites.mass_delete(
    site_ids=[1, 2, 3, 4, 5],
    dry_run=False,  # Execute actual deletion
    continue_on_error=True  # Continue even if some fail
)

print(f"Successfully deleted: {result['success_count']}")
print(f"Failed to delete: {result['failure_count']}")

# Check failures
for failure in result['failures']:
    print(f"Failed: {failure['name']} - {failure['error']}")
```

### Delete by Pattern

```python
# Preview deletion of empty sites matching pattern
result = client.sites.delete_by_pattern(
    name_pattern='sn_',
    empty_only=True,
    dry_run=True  # Preview first
)

print(f"Would delete {len(result['preview'])} sites")

# If satisfied, execute the deletion
result = client.sites.delete_by_pattern(
    name_pattern='sn_',
    empty_only=True,
    dry_run=False  # Actually delete
)

print(f"Deleted {result['success_count']} sites")
```

## Advanced Operations

### Get Scan Template

```python
# Get the scan template for a site
template = client.sites.get_scan_template(site_id=123)
print(f"Scan template: {template['name']}")
```

### Get Scan Engine

```python
# Get the scan engine for a site
engine = client.sites.get_scan_engine(site_id=123)
print(f"Scan engine: {engine['name']}")
```

## Common Use Cases

### Cleanup Empty Sites

```python
# Find and delete all empty sites
empty_sites = client.sites.filter_empty_sites()
print(f"Found {len(empty_sites)} empty sites")

if empty_sites:
    site_ids = [s['id'] for s in empty_sites]
    
    # Preview first
    preview = client.sites.mass_delete(site_ids, dry_run=True)
    print("Preview:")
    for site in preview['preview']:
        print(f"  - {site['name']}")
    
    # Get confirmation
    confirm = input("Delete these sites? (yes/no): ")
    if confirm.lower() == 'yes':
        result = client.sites.mass_delete(site_ids, dry_run=False)
        print(f"Deleted {result['success_count']} empty sites")
```

### Cleanup Sites by Naming Convention

```python
# Find sites with old naming convention and delete empty ones
old_sites = client.sites.filter_sites(
    name_pattern='old_',
    empty_only=True
)

print(f"Found {len(old_sites)} old empty sites")

# Delete with pattern (includes preview)
result = client.sites.delete_by_pattern(
    name_pattern='old_',
    empty_only=True,
    dry_run=False
)

print(f"Cleanup complete:")
print(f"  Deleted: {result['success_count']}")
print(f"  Failed: {result['failure_count']}")
```

### Audit Site Assets

```python
# Audit all sites and their asset counts
all_sites = client.sites.get_all()

site_audit = []
for site in all_sites:
    asset_count = client.sites.get_asset_count(site['id'])
    site_audit.append({
        'id': site['id'],
        'name': site['name'],
        'asset_count': asset_count
    })

# Sort by asset count
site_audit.sort(key=lambda x: x['asset_count'], reverse=True)

print("Site Asset Audit:")
for site in site_audit:
    print(f"{site['name']}: {site['asset_count']} assets")
```

## Error Handling

```python
from requests.exceptions import HTTPError

try:
    site = client.sites.get_site(999999)
except HTTPError as e:
    if e.response.status_code == 404:
        print("Site not found")
    else:
        print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Always Preview First**: Use `dry_run=True` before mass deletions
2. **Handle Errors Gracefully**: Use `continue_on_error=True` for bulk operations
3. **Filter Before Delete**: Use filtering to target specific sites
4. **Check Asset Counts**: Verify sites are empty before deletion
5. **Use Context Managers**: Use `with InsightVMClient() as client:` for automatic cleanup

## Safety Features

The Site Management module includes several safety features:

- **Dry Run Mode**: Default `dry_run=True` for mass operations
- **Preview**: Always shows what will be affected before execution
- **Error Handling**: Continues operation even if individual sites fail
- **Validation**: Retrieves site details before deletion
- **Logging**: Comprehensive logging of all operations

## Examples

See `/docs/EXAMPLES.md` for complete working examples of site management operations.

## API Reference

For detailed API documentation, see `/docs/API_REFERENCE.md`.
