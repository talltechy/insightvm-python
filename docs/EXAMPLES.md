# Usage Examples

Practical examples for common InsightVM-Python v2.0 workflows.

## Table of Contents

- [Basic Setup](#basic-setup)
- [Asset Management](#asset-management)
- [Asset Groups](#asset-groups)
- [Search and Filtering](#search-and-filtering)
- [Vulnerability Management](#vulnerability-management)
- [Tag Management](#tag-management)
- [Batch Operations](#batch-operations)
- [Error Handling](#error-handling)
- [Advanced Patterns](#advanced-patterns)

---

## Basic Setup

### Simple Configuration

```python
from rapid7 import InsightVMClient

# Using environment variables from .env
client = InsightVMClient()

# Verify connection
assets = client.assets.list(page=0, size=1)
print(f"✅ Connected! Total assets: {assets['page']['totalResources']}")
```

### Explicit Configuration

```python
from rapid7 import InsightVMClient

# Provide credentials directly
client = InsightVMClient(
    username="your_username",
    password="your_password",
    base_url="https://console:3780",
    verify_ssl=False,  # For self-signed certificates
    timeout=(10, 90)   # Connect and read timeouts
)
```

### Using Context Manager

```python
from rapid7 import InsightVMClient

# Automatic cleanup when done
with InsightVMClient() as client:
    assets = client.assets.list()
    # Client automatically cleaned up after this block
```

---

## Asset Management

### List All Assets

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Get first page
result = client.assets.list(page=0, size=100)

print(f"Total assets: {result['page']['totalResources']}")
print(f"This page: {result['page']['size']}")

for asset in result['resources']:
    print(f"- {asset['id']}: {asset['ip']} ({asset['hostname']})")
```

### Get Specific Asset

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Get asset by ID
asset_id = 123
asset = client.assets.get_asset(asset_id)

# Display details
print(f"Asset: {asset['hostname']}")
print(f"IP: {asset['ip']}")
print(f"OS: {asset['os']}")
print(f"Risk Score: {asset['riskScore']}")
print(f"Vulnerabilities: {asset['vulnerabilities']['total']}")
```

### Get All Assets (Auto-Pagination)

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Automatically handles pagination
all_assets = client.assets.get_all(batch_size=500)

print(f"Retrieved {len(all_assets)} total assets")

# Process assets
for asset in all_assets:
    if asset['riskScore'] > 50000:
        print(f"⚠️ High risk: {asset['hostname']} (score: {asset['riskScore']})")
```

### Sort Assets

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Sort by risk score (descending)
assets = client.assets.list(
    page=0,
    size=50,
    sort=["riskScore,DESC"]
)

print("Top 50 riskiest assets:")
for asset in assets['resources']:
    print(f"{asset['riskScore']:>6} - {asset['hostname']}")
```

---

## Asset Groups

### List All Asset Groups

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

groups = client.asset_groups.list()

print(f"Total groups: {len(groups['resources'])}")

for group in groups['resources']:
    print(f"- {group['name']}: {group['assets']} assets")
```

### Create Dynamic Asset Group

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Create group for Windows servers with critical vulns
group = client.asset_groups.create(
    name="Critical Windows Servers",
    description="Windows servers with critical vulnerabilities",
    search_criteria={
        "filters": [
            {
                "field": "operating-system",
                "operator": "contains",
                "value": "Windows Server"
            },
            {
                "field": "cvss-score",
                "operator": "is-greater-than",
                "value": 9.0
            }
        ],
        "match": "all"
    }
)

print(f"Created group: {group['name']} (ID: {group['id']})")
```

### Create High-Risk Asset Group

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Convenient method for high-risk groups
group = client.asset_groups.create_high_risk(
    name="Critical Assets",
    description="Assets with risk score > 30000",
    threshold=30000
)

print(f"Created: {group['name']} with {group['assets']} assets")
```

### Update Asset Group

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

group_id = 42

# Update group properties
updated = client.asset_groups.update(
    group_id=group_id,
    name="Updated Group Name",
    description="Updated description",
    search_criteria={
        "filters": [
            {
                "field": "risk-score",
                "operator": "is-greater-than",
                "value": 40000
            }
        ],
        "match": "all"
    }
)

print(f"Updated: {updated['name']}")
```

### Delete Asset Group

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

group_id = 42

# Delete the group
client.asset_groups.delete_group(group_id)
print(f"Deleted group {group_id}")
```

### Manage Static Group Members

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

group_id = 10
asset_id = 123

# Add asset to group
client.asset_groups.add_asset(group_id, asset_id)
print(f"Added asset {asset_id} to group {group_id}")

# Get group members
assets = client.asset_groups.get_assets(group_id)
print(f"Group has {len(assets['resources'])} members")

# Remove asset from group
client.asset_groups.remove_asset(group_id, asset_id)
print(f"Removed asset {asset_id} from group {group_id}")
```

---

## Search and Filtering

### Search by Risk Score

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Find high-risk assets
results = client.assets.search({
    "filters": [
        {
            "field": "risk-score",
            "operator": "is-greater-than",
            "value": 20000
        }
    ],
    "match": "all"
})

print(f"Found {len(results['resources'])} high-risk assets")
```

### Search by Operating System

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Find all Windows systems
results = client.assets.search({
    "filters": [
        {
            "field": "operating-system",
            "operator": "contains",
            "value": "Windows"
        }
    ],
    "match": "all"
})

print(f"Found {len(results['resources'])} Windows systems")
```

### Complex Search with Multiple Criteria

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Find critical Linux servers
results = client.assets.search({
    "filters": [
        {
            "field": "operating-system",
            "operator": "contains",
            "value": "Linux"
        },
        {
            "field": "host-type",
            "operator": "is",
            "value": "HYPERVISOR"
        },
        {
            "field": "cvss-score",
            "operator": "is-greater-than",
            "value": 7.0
        }
    ],
    "match": "all"  # All conditions must be true
})

print(f"Critical Linux hypervisors: {len(results['resources'])}")

for asset in results['resources']:
    print(f"- {asset['hostname']}: Risk {asset['riskScore']}")
```

### Search by IP Address Range

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Find assets in specific subnet
results = client.assets.search({
    "filters": [
        {
            "field": "ip-address",
            "operator": "in-range",
            "lower": "192.168.1.0",
            "upper": "192.168.1.255"
        }
    ],
    "match": "all"
})

print(f"Assets in 192.168.1.0/24: {len(results['resources'])}")
```

---

## Vulnerability Management

### Get Asset Vulnerabilities

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

asset_id = 123

# Get all vulnerabilities for an asset
vulns = client.assets.get_vulnerabilities(asset_id)

print(f"Total vulnerabilities: {vulns['page']['totalResources']}")
print(f"Critical: {len([v for v in vulns['resources'] if v['severity'] == 'Critical'])}")
print(f"Severe: {len([v for v in vulns['resources'] if v['severity'] == 'Severe'])}")
```

### Find Assets with Specific Vulnerability

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Search for assets with a specific CVE
vulnerability_id = "CVE-2021-44228"  # Log4j

results = client.assets.search({
    "filters": [
        {
            "field": "vulnerability-id",
            "operator": "is",
            "value": vulnerability_id
        }
    ],
    "match": "all"
})

print(f"Assets affected by {vulnerability_id}: {len(results['resources'])}")

for asset in results['resources']:
    print(f"- {asset['hostname']} ({asset['ip']})")
```

### Generate Vulnerability Report

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Get all assets
all_assets = client.assets.get_all()

# Categorize by risk
risk_categories = {
    'critical': [],
    'high': [],
    'medium': [],
    'low': []
}

for asset in all_assets:
    score = asset['riskScore']
    if score > 50000:
        risk_categories['critical'].append(asset)
    elif score > 20000:
        risk_categories['high'].append(asset)
    elif score > 5000:
        risk_categories['medium'].append(asset)
    else:
        risk_categories['low'].append(asset)

# Print summary
print("Vulnerability Risk Summary")
print("=" * 50)
print(f"Critical: {len(risk_categories['critical'])} assets")
print(f"High:     {len(risk_categories['high'])} assets")
print(f"Medium:   {len(risk_categories['medium'])} assets")
print(f"Low:      {len(risk_categories['low'])} assets")
```

---

## Tag Management

### Get Asset Tags

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

asset_id = 123

# Get tags for an asset
tags = client.assets.get_tags(asset_id)

print(f"Tags for asset {asset_id}:")
for tag in tags['resources']:
    print(f"- {tag['name']}")
```

### Add Tag to Asset

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

asset_id = 123
tag_id = 5

# Add tag
client.assets.add_tag(asset_id, tag_id)
print(f"Added tag {tag_id} to asset {asset_id}")
```

### Remove Tag from Asset

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

asset_id = 123
tag_id = 5

# Remove tag
client.assets.remove_tag(asset_id, tag_id)
print(f"Removed tag {tag_id} from asset {asset_id}")
```

### Bulk Tag Operations

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Tag all high-risk assets
tag_id = 10  # "High Risk" tag
threshold = 30000

all_assets = client.assets.get_all()

tagged_count = 0
for asset in all_assets:
    if asset['riskScore'] > threshold:
        try:
            client.assets.add_tag(asset['id'], tag_id)
            tagged_count += 1
        except Exception as e:
            print(f"Error tagging asset {asset['id']}: {e}")

print(f"Tagged {tagged_count} high-risk assets")
```

---

## Batch Operations

### Process Assets in Batches

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

def process_batch(assets):
    """Process a batch of assets"""
    for asset in assets:
        # Your processing logic here
        print(f"Processing {asset['hostname']}...")

# Process in batches of 100
page = 0
batch_size = 100

while True:
    result = client.assets.list(page=page, size=batch_size)
    assets = result['resources']
    
    if not assets:
        break
    
    process_batch(assets)
    page += 1
    
    print(f"Processed page {page} ({len(assets)} assets)")
```

### Export Assets to CSV

```python
from rapid7 import InsightVMClient
import csv

client = InsightVMClient()

# Get all assets
all_assets = client.assets.get_all()

# Export to CSV
with open('assets_export.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'hostname', 'ip', 'os', 'riskScore', 'vulnerabilities']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for asset in all_assets:
        writer.writerow({
            'id': asset['id'],
            'hostname': asset.get('hostname', 'N/A'),
            'ip': asset.get('ip', 'N/A'),
            'os': asset.get('os', 'N/A'),
            'riskScore': asset.get('riskScore', 0),
            'vulnerabilities': asset.get('vulnerabilities', {}).get('total', 0)
        })

print(f"Exported {len(all_assets)} assets to assets_export.csv")
```

### Create Multiple Asset Groups

```python
from rapid7 import InsightVMClient

client = InsightVMClient()

# Define groups to create
groups_config = [
    {
        'name': 'Web Servers',
        'threshold': 15000,
        'os_filter': 'Web Server'
    },
    {
        'name': 'Database Servers',
        'threshold': 25000,
        'os_filter': 'Database'
    },
    {
        'name': 'Domain Controllers',
        'threshold': 35000,
        'os_filter': 'Domain Controller'
    }
]

created_groups = []

for config in groups_config:
    try:
        group = client.asset_groups.create(
            name=config['name'],
            description=f"Automated group for {config['name']}",
            search_criteria={
                "filters": [
                    {
                        "field": "risk-score",
                        "operator": "is-greater-than",
                        "value": config['threshold']
                    },
                    {
                        "field": "operating-system",
                        "operator": "contains",
                        "value": config['os_filter']
                    }
                ],
                "match": "all"
            }
        )
        created_groups.append(group)
        print(f"✅ Created: {group['name']} ({group['assets']} assets)")
    except Exception as e:
        print(f"❌ Failed to create {config['name']}: {e}")

print(f"\nSuccessfully created {len(created_groups)} groups")
```

---

## Error Handling

### Basic Error Handling

```python
from rapid7 import InsightVMClient
import requests

try:
    client = InsightVMClient()
    assets = client.assets.list()
    print(f"Success! Got {len(assets['resources'])} assets")
    
except ValueError as e:
    # Configuration error
    print(f"❌ Configuration error: {e}")
    print("Check your .env file")
    
except requests.exceptions.HTTPError as e:
    # HTTP error
    print(f"❌ API error: {e}")
    print(f"Status code: {e.response.status_code}")
    
except Exception as e:
    # Unexpected error
    print(f"❌ Unexpected error: {e}")
```

### Comprehensive Error Handling

```python
from rapid7 import InsightVMClient
import requests
import time

def safe_api_call(func, *args, max_retries=3, **kwargs):
    """Execute API call with retry logic"""
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
            
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            
            if status == 429:  # Rate limit
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
                
            elif status == 401:
                print("Authentication failed")
                raise
                
            elif status == 404:
                print("Resource not found")
                raise
                
            else:
                print(f"HTTP error {status}")
                raise
                
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Connection error. Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            raise
            
        except requests.exceptions.Timeout as e:
            if attempt < max_retries - 1:
                print(f"Timeout. Retrying...")
                continue
            raise
    
    raise Exception(f"Failed after {max_retries} attempts")

# Usage
client = InsightVMClient()
assets = safe_api_call(client.assets.list, page=0, size=100)
```

---

## Advanced Patterns

### Parallel Processing with Thread Pool

```python
from rapid7 import InsightVMClient
from concurrent.futures import ThreadPoolExecutor, as_completed

client = InsightVMClient()

def get_asset_details(asset_id):
    """Get detailed information for an asset"""
    try:
        asset = client.assets.get_asset(asset_id)
        vulns = client.assets.get_vulnerabilities(asset_id)
        return {
            'id': asset_id,
            'hostname': asset.get('hostname'),
            'vuln_count': len(vulns['resources'])
        }
    except Exception as e:
        return {'id': asset_id, 'error': str(e)}

# Get list of asset IDs
assets = client.assets.list(page=0, size=100)
asset_ids = [asset['id'] for asset in assets['resources']]

# Process in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(get_asset_details, aid): aid for aid in asset_ids}
    
    for future in as_completed(futures):
        result = future.result()
        if 'error' not in result:
            print(f"{result['hostname']}: {result['vuln_count']} vulnerabilities")
```

### Caching Results

```python
from rapid7 import InsightVMClient
from functools import lru_cache
import hashlib
import json

client = InsightVMClient()

@lru_cache(maxsize=100)
def get_cached_asset(asset_id):
    """Get asset with caching"""
    return json.dumps(client.assets.get_asset(asset_id))

# First call - hits API
asset1 = json.loads(get_cached_asset(123))
print(f"First call: {asset1['hostname']}")

# Second call - uses cache
asset2 = json.loads(get_cached_asset(123))
print(f"Cached call: {asset2['hostname']}")
```

### Progress Tracking

```python
from rapid7 import InsightVMClient
from tqdm import tqdm

client = InsightVMClient()

# Get total count
first_page = client.assets.list(page=0, size=1)
total = first_page['page']['totalResources']

# Process with progress bar
all_assets = []
batch_size = 500

with tqdm(total=total, desc="Fetching assets") as pbar:
    page = 0
    while len(all_assets) < total:
        result = client.assets.list(page=page, size=batch_size)
        assets = result['resources']
        
        if not assets:
            break
        
        all_assets.extend(assets)
        pbar.update(len(assets))
        page += 1

print(f"\nRetrieved {len(all_assets)} assets")
```

### Custom API Module

```python
from rapid7.api.base import BaseAPI
from rapid7.auth import InsightVMAuth

class CustomAPI(BaseAPI):
    """Custom API module extending BaseAPI"""
    
    def get_custom_data(self, param):
        """Custom method using base request functionality"""
        return self._request('GET', f'/custom/endpoint/{param}')

# Usage
auth = InsightVMAuth()
custom_api = CustomAPI(auth)
data = custom_api.get_custom_data('value')
```

---

## See Also

- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Migration Guide](../MIGRATION.md) - Upgrading from v1.0
- [Contributing](../CONTRIBUTING.md) - Development guidelines
