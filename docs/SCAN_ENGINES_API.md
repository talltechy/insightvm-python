# Scan Engines API Documentation

## Overview

The Scan Engines API module provides comprehensive functionality for managing scan engines and engine pools in Rapid7 InsightVM. This includes creating, updating, and deleting engines and pools, monitoring engine health, and managing site assignments.

## Quick Start

```python
from rapid7 import InsightVMClient

# Initialize client
client = InsightVMClient()

# List all scan engines
engines = client.scan_engines.list()
for engine in engines['resources']:
    print(f"{engine['name']}: {engine['status']}")

# Get specific engine details
engine = client.scan_engines.get(engine_id=6)
print(f"Engine: {engine['name']} at {engine['address']}")

# Create an engine pool
pool = client.scan_engines.create_pool(
    name="Production Pool",
    engine_ids=[1, 2, 3]
)
print(f"Created pool: {pool['id']}")
```

## Scan Engine Operations

### List All Scan Engines

List all scan engines available for scanning:

```python
engines = client.scan_engines.list()

for engine in engines['resources']:
    print(f"ID: {engine['id']}")
    print(f"Name: {engine['name']}")
    print(f"Address: {engine['address']}")
    print(f"Port: {engine['port']}")
    print(f"Status: {engine['status']}")
    print(f"Product Version: {engine['productVersion']}")
    print(f"Content Version: {engine['contentVersion']}")
    print(f"Sites: {engine['sites']}")
    print(f"Is AWS Pre-Auth: {engine['isAWSPreAuthEngine']}")
    print("---")
```

### Get Scan Engine Details

Retrieve detailed information for a specific scan engine:

```python
engine = client.scan_engines.get(engine_id=6)

print(f"Engine Name: {engine['name']}")
print(f"Address: {engine['address']}:{engine['port']}")
print(f"Status: {engine['status']}")
print(f"Assigned to {len(engine['sites'])} sites")
```

### Update Scan Engine

Update scan engine configuration:

```python
result = client.scan_engines.update(
    engine_id=6,
    name="Updated Engine Name"
)
```

### Delete Scan Engine

Remove a scan engine from the system:

```python
# Engine must not be actively scanning or assigned to sites
result = client.scan_engines.delete(engine_id=6)
```

## Engine Site Operations

### Get Sites Assigned to Engine

List all sites assigned to a specific scan engine:

```python
sites = client.scan_engines.get_sites(
    engine_id=6,
    page=0,
    size=50,
    sort=['name,ASC']
)

print(f"Total sites: {sites['page']['totalResources']}")
for site in sites['resources']:
    print(f"- {site['name']} (ID: {site['id']})")
```

### Get Scans Run on Engine

Retrieve scans that have been executed on a specific engine:

```python
scans = client.scan_engines.get_scans(
    engine_id=6,
    page=0,
    size=20
)

for scan in scans['resources']:
    print(f"Scan {scan['id']}: {scan['status']}")
```

## Engine Pool Operations

### List All Engine Pools

List all available engine pools:

```python
pools = client.scan_engines.list_pools()

for pool in pools['resources']:
    print(f"Pool: {pool['name']}")
    print(f"Engines: {pool['engines']}")
    print(f"Sites: {pool['sites']}")
    print("---")
```

### Get Engine Pool Details

Retrieve details for a specific engine pool:

```python
pool = client.scan_engines.get_pool(pool_id=6)

print(f"Pool Name: {pool['name']}")
print(f"Engines in pool: {pool['engines']}")
print(f"Sites using pool: {pool['sites']}")
```

### Create Engine Pool

Create a new engine pool for load balancing:

```python
# Create pool with engines
pool = client.scan_engines.create_pool(
    name="Production Pool",
    engine_ids=[1, 2, 3]
)
print(f"Created pool {pool['id']}")

# Create empty pool (add engines later)
pool = client.scan_engines.create_pool(
    name="Development Pool"
)
```

### Update Engine Pool

Update an existing engine pool:

```python
result = client.scan_engines.update_pool(
    pool_id=6,
    name="Updated Pool Name",
    engines=[1, 2, 3, 4, 5]
)
```

### Delete Engine Pool

Remove an engine pool:

```python
result = client.scan_engines.delete_pool(pool_id=6)
```

### Manage Pool Engines

Get and set engines in a pool:

```python
# Get current engines in pool
engines = client.scan_engines.get_pool_engines(pool_id=6)
print(f"Pool has {len(engines['resources'])} engines")

# Replace engines in pool
result = client.scan_engines.set_pool_engines(
    pool_id=6,
    engine_ids=[1, 2, 3, 4, 5]
)
```

### Get Pools for an Engine

Find all pools that a scan engine belongs to:

```python
pools = client.scan_engines.get_engine_pools(engine_id=6)

for pool in pools['resources']:
    print(f"Engine is in pool: {pool['name']}")
```

## Shared Secret Operations

### Revoke Shared Secret

Revoke the current shared secret used for pairing engines:

```python
# Prevents new engines from being paired
result = client.scan_engines.delete_shared_secret()
```

## Helper Methods

### Get Available Engines

Filter engines by status to get only available ones:

```python
available = client.scan_engines.get_available_engines()
print(f"{len(available)} engines available for scanning")

for engine in available:
    print(f"- {engine['name']}: {engine['status']}")
```

### Get Engine Summary

Get a comprehensive summary including sites and pools:

```python
summary = client.scan_engines.get_engine_summary(engine_id=6)

print(f"Engine: {summary['engine']['name']}")
print(f"Total Sites: {summary['sites_count']}")
print(f"Pools: {len(summary['pools'])}")

for pool in summary['pools']:
    print(f"- In pool: {pool['name']}")
```

### Assign Engine to Pool

Add an engine to an existing pool:

```python
result = client.scan_engines.assign_engine_to_pool(
    engine_id=6,
    pool_id=2
)
print("Engine assigned to pool")
```

### Remove Engine from Pool

Remove an engine from a pool:

```python
result = client.scan_engines.remove_engine_from_pool(
    engine_id=6,
    pool_id=2
)
print("Engine removed from pool")
```

## Common Use Cases

### Monitor Engine Health

Check the status and health of all scan engines:

```python
engines = client.scan_engines.list()

for engine in engines['resources']:
    status = engine['status'].lower()
    name = engine['name']
    
    if status in ['active', 'running']:
        print(f"✓ {name}: Healthy")
    else:
        print(f"✗ {name}: {status}")
```

### Create Load-Balanced Scanning Infrastructure

Set up engine pools for distributed scanning:

```python
# Get all available engines
available = client.scan_engines.get_available_engines()
engine_ids = [e['id'] for e in available]

# Split engines into pools
half = len(engine_ids) // 2

# Create production pool
prod_pool = client.scan_engines.create_pool(
    name="Production Pool",
    engine_ids=engine_ids[:half]
)

# Create development pool
dev_pool = client.scan_engines.create_pool(
    name="Development Pool",
    engine_ids=engine_ids[half:]
)

print(f"Production Pool: {len(engine_ids[:half])} engines")
print(f"Development Pool: {len(engine_ids[half:])} engines")
```

### Audit Engine Assignments

Review which engines are assigned to which sites:

```python
engines = client.scan_engines.list()

for engine in engines['resources']:
    print(f"\nEngine: {engine['name']}")
    
    sites = client.scan_engines.get_sites(
        engine_id=engine['id'],
        size=100
    )
    
    print(f"Assigned to {sites['page']['totalResources']} sites:")
    for site in sites['resources']:
        print(f"  - {site['name']}")
```

### Reorganize Engine Pools

Move engines between pools:

```python
# Remove engine from old pool
client.scan_engines.remove_engine_from_pool(
    engine_id=6,
    pool_id=1  # Old pool
)

# Add engine to new pool
client.scan_engines.assign_engine_to_pool(
    engine_id=6,
    pool_id=2  # New pool
)

print("Engine moved to new pool")
```

## Error Handling

Handle common error scenarios:

```python
from requests.exceptions import HTTPError

try:
    engine = client.scan_engines.get(engine_id=999)
except HTTPError as e:
    if e.response.status_code == 404:
        print("Engine not found")
    elif e.response.status_code == 401:
        print("Authentication failed")
    else:
        print(f"Error: {e}")
```

## Response Examples

### Engine Response

```json
{
  "id": 6,
  "name": "Corporate Scan Engine 001",
  "address": "corporate-scan-engine-001.acme.com",
  "port": 40894,
  "status": "active",
  "productVersion": "6.6.123",
  "contentVersion": "2024-10-07",
  "serialNumber": "ABC123DEF456",
  "isAWSPreAuthEngine": false,
  "sites": [42, 43, 44],
  "lastRefreshedDate": "2024-10-07T12:00:00Z",
  "lastUpdatedDate": "2024-10-07T12:00:00Z",
  "links": [
    {
      "href": "https://hostname:3780/api/3/scan_engines/6",
      "rel": "self"
    }
  ]
}
```

### Engine Pool Response

```json
{
  "id": 6,
  "name": "Corporate Scan Engine Pool 001",
  "engines": [1, 2, 3],
  "sites": [42, 43, 44],
  "links": [
    {
      "href": "https://hostname:3780/api/3/scan_engine_pools/6",
      "rel": "self"
    }
  ]
}
```

## API Methods Reference

### Scan Engine Operations
- `list(**params)` - List all scan engines
- `get(engine_id)` - Get engine details
- `update(engine_id, **kwargs)` - Update engine
- `delete(engine_id)` - Delete engine
- `get_sites(engine_id, page, size, sort)` - Get assigned sites
- `get_scans(engine_id, page, size, sort)` - Get executed scans

### Engine Pool Operations
- `list_pools(**params)` - List all engine pools
- `get_pool(pool_id)` - Get pool details
- `create_pool(name, engine_ids, **kwargs)` - Create pool
- `update_pool(pool_id, **kwargs)` - Update pool
- `delete_pool(pool_id)` - Delete pool
- `get_pool_engines(pool_id)` - Get engines in pool
- `set_pool_engines(pool_id, engine_ids)` - Set pool engines
- `get_engine_pools(engine_id)` - Get pools for engine

### Shared Secret Operations
- `delete_shared_secret()` - Revoke shared secret

### Helper Methods
- `get_available_engines()` - Get active engines
- `get_engine_summary(engine_id)` - Get comprehensive summary
- `assign_engine_to_pool(engine_id, pool_id)` - Assign to pool
- `remove_engine_from_pool(engine_id, pool_id)` - Remove from pool

## Best Practices

1. **Monitor Engine Health**: Regularly check engine status
2. **Use Engine Pools**: Distribute load across multiple engines
3. **Plan Capacity**: Ensure engines can handle site assignments
4. **Audit Assignments**: Regularly review engine-to-site mappings
5. **Secure Pairing**: Manage shared secrets carefully

## See Also

- [Sites API Documentation](SITE_MANAGEMENT.md) - Managing sites that use engines
- [Scans API Documentation](SCANS_API.md) - Managing scans run on engines
- [API Reference](API_REFERENCE.md) - Complete API documentation
