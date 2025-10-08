# Solutions API Documentation

Complete guide to the InsightVM Solutions API module for managing remediation solutions.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Core Operations](#core-operations)
- [Common Use Cases](#common-use-cases)
- [Best Practices](#best-practices)
- [Response Examples](#response-examples)
- [API Reference](#api-reference)

## Overview

The Solutions API provides access to remediation solutions that address vulnerabilities in InsightVM. Solutions represent patches, configuration changes, or other actions that can resolve security vulnerabilities.

### Key Features

- **List Solutions**: Browse all available remediation solutions
- **Get Solution Details**: Access detailed remediation steps and information
- **Prerequisites Management**: Understand solution dependencies
- **Superseding Relationships**: Find newer or better alternative solutions
- **Filtering Capabilities**: Search by type, platform, or applicability

### Solution Types

1. **Configuration**: Configuration changes or workarounds
2. **Patch**: Software patches or updates
3. **Rollup**: Cumulative updates containing multiple fixes

## Quick Start

```python
from rapid7 import InsightVMClient

# Create client
client = InsightVMClient()

# List solutions
solutions = client.solutions.list(size=100)
print(f"Total solutions: {solutions['page']['totalResources']}")

# Get solution details
solution = client.solutions.get_solution('ubuntu-upgrade-libexpat1')
print(f"Title: {solution['summary']['text']}")
print(f"Steps: {solution['steps']['text']}")
print(f"Estimate: {solution['estimate']}")

# Get prerequisites
prereqs = client.solutions.get_prerequisites('solution-id')
for prereq in prereqs['resources']:
    print(f"Required first: {prereq['summary']['text']}")
```

## Core Operations

### List All Solutions

Retrieve paginated list of all available solutions:

```python
# Basic listing
solutions = client.solutions.list(page=0, size=500)

# With sorting
solutions = client.solutions.list(
    page=0,
    size=100,
    sort=["id,ASC"]
)

# Process results
for solution in solutions['resources']:
    print(f"{solution['id']}: {solution['summary']['text']}")
    print(f"  Type: {solution['type']}")
    print(f"  Applies to: {solution['appliesTo']}")
```

### Get Solution Details

Retrieve detailed information for a specific solution:

```python
solution = client.solutions.get_solution('ubuntu-upgrade-libexpat1')

# Access solution information
print(f"ID: {solution['id']}")
print(f"Summary: {solution['summary']['text']}")
print(f"Applies to: {solution['appliesTo']}")
print(f"Type: {solution['type']}")
print(f"Estimate: {solution['estimate']}")

# Get remediation steps
print(f"\nSteps:")
print(solution['steps']['text'])

# Additional information
if 'additionalInformation' in solution:
    print(f"\nAdditional Info:")
    print(solution['additionalInformation']['text'])
```

### Get Prerequisites

Find solutions that must be executed first:

```python
prereqs = client.solutions.get_prerequisites('solution-id')

if prereqs['resources']:
    print("Prerequisites required:")
    for prereq in prereqs['resources']:
        print(f"  - {prereq['summary']['text']}")
        print(f"    ID: {prereq['id']}")
else:
    print("No prerequisites required")
```

### Get Superseding Solutions

Find newer or better alternative solutions:

```python
# Get all superseding solutions
newer_solutions = client.solutions.get_superseding_solutions('old-solution-id')

# Get only rollup superseding solutions
rollups = client.solutions.get_superseding_solutions(
    'old-solution-id',
    rollup_only=True
)

for solution in newer_solutions['resources']:
    print(f"Newer alternative: {solution['summary']['text']}")
    print(f"  ID: {solution['id']}")
    print(f"  Type: {solution['type']}")
```

### Get Superseded Solutions

Find older solutions replaced by this one:

```python
older = client.solutions.get_superseded_solutions('new-solution-id')

for solution in older['resources']:
    print(f"This replaces: {solution['summary']['text']}")
```

## Common Use Cases

### Use Case 1: Build Remediation Priority List

Create prioritized remediation list based on solution types:

```python
# Get all solutions
all_solutions = client.solutions.get_all_solutions(sort=["id,ASC"])

# Categorize by type
config_solutions = []
patch_solutions = []
rollup_solutions = []

for solution in all_solutions:
    sol_type = solution.get('type', '').lower()
    if sol_type == 'configuration':
        config_solutions.append(solution)
    elif sol_type == 'patch':
        patch_solutions.append(solution)
    elif sol_type == 'rollup':
        rollup_solutions.append(solution)

# Prioritize rollups (most comprehensive)
print(f"\nPriority 1: Rollup Solutions ({len(rollup_solutions)})")
for solution in rollup_solutions[:5]:
    print(f"  - {solution['summary']['text']}")

# Then patches
print(f"\nPriority 2: Patch Solutions ({len(patch_solutions)})")
for solution in patch_solutions[:5]:
    print(f"  - {solution['summary']['text']}")

# Finally configurations
print(f"\nPriority 3: Configuration Solutions ({len(config_solutions)})")
for solution in config_solutions[:5]:
    print(f"  - {solution['summary']['text']}")
```

### Use Case 2: Generate Remediation Playbook

Create detailed remediation documentation:

```python
def generate_remediation_playbook(solution_id: str):
    """Generate detailed playbook for a solution."""
    
    # Get solution details
    solution = client.solutions.get_solution(solution_id)
    
    print(f"# Remediation Playbook: {solution['summary']['text']}")
    print(f"\n**Solution ID:** {solution['id']}")
    print(f"**Type:** {solution['type']}")
    print(f"**Applies To:** {solution['appliesTo']}")
    print(f"**Estimated Time:** {solution['estimate']}")
    
    # Check for prerequisites
    prereqs = client.solutions.get_prerequisites(solution_id)
    if prereqs['resources']:
        print("\n## Prerequisites")
        print("Execute these solutions first:")
        for i, prereq in enumerate(prereqs['resources'], 1):
            print(f"{i}. {prereq['summary']['text']} ({prereq['id']})")
    
    # Remediation steps
    print("\n## Remediation Steps")
    print(solution['steps']['text'])
    
    # Additional information
    if solution.get('additionalInformation', {}).get('text'):
        print("\n## Additional Information")
        print(solution['additionalInformation']['text'])
    
    # Check for superseding solutions
    superseding = client.solutions.get_superseding_solutions(solution_id)
    if superseding['resources']:
        print("\n## Note: Newer Solutions Available")
        for newer in superseding['resources']:
            print(f"- {newer['summary']['text']} ({newer['id']})")

# Generate playbook
generate_remediation_playbook('ubuntu-upgrade-libexpat1')
```

### Use Case 3: Platform-Specific Remediation

Find solutions for specific platforms:

```python
# Find Ubuntu solutions
ubuntu_solutions = client.solutions.search_by_applies_to('Ubuntu')

print(f"Ubuntu Solutions: {len(ubuntu_solutions)}")
for solution in ubuntu_solutions[:10]:
    print(f"\n{solution['summary']['text']}")
    print(f"  ID: {solution['id']}")
    print(f"  Applies to: {solution['appliesTo']}")
    print(f"  Estimate: {solution.get('estimate', 'N/A')}")

# Find Windows solutions
windows_solutions = client.solutions.search_by_applies_to('Windows')
print(f"\nWindows Solutions: {len(windows_solutions)}")
```

### Use Case 4: Solution Dependency Analysis

Analyze solution dependencies and relationships:

```python
def analyze_solution_dependencies(solution_id: str, level: int = 0):
    """Recursively analyze solution dependencies."""
    indent = "  " * level
    
    # Get solution details
    solution = client.solutions.get_solution(solution_id)
    print(f"{indent}- {solution['summary']['text']} ({solution_id})")
    
    # Check prerequisites
    prereqs = client.solutions.get_prerequisites(solution_id)
    if prereqs['resources']:
        print(f"{indent}  Prerequisites:")
        for prereq in prereqs['resources']:
            # Recursively analyze prerequisites
            analyze_solution_dependencies(prereq['id'], level + 2)

# Analyze dependencies
print("Solution Dependency Tree:")
analyze_solution_dependencies('solution-with-dependencies')
```

### Use Case 5: Solution Effectiveness Tracking

Track which solutions address the most vulnerabilities:

```python
# This would typically be combined with Vulnerabilities API
# to show which solutions are most impactful

def get_solution_impact(solution_id: str):
    """Get impact information for a solution."""
    solution = client.solutions.get_solution(solution_id)
    
    # Check what this solution supersedes
    superseded = client.solutions.get_superseded_solutions(solution_id)
    
    # Check if there are newer solutions
    superseding = client.solutions.get_superseding_solutions(solution_id)
    
    return {
        'id': solution_id,
        'summary': solution['summary']['text'],
        'type': solution['type'],
        'supersedes_count': len(superseded.get('resources', [])),
        'has_newer': len(superseding.get('resources', [])) > 0
    }

# Analyze top solutions
solutions = client.solutions.list(size=50)
for solution in solutions['resources'][:10]:
    impact = get_solution_impact(solution['id'])
    print(f"\n{impact['summary']}")
    print(f"  Type: {impact['type']}")
    print(f"  Supersedes: {impact['supersedes_count']} older solutions")
    print(f"  Has newer: {impact['has_newer']}")
```

## Best Practices

### 1. Solution Prioritization

```python
# Always check for superseding solutions first
solution_id = 'potential-solution'

# Check if there's a newer version
superseding = client.solutions.get_superseding_solutions(
    solution_id,
    rollup_only=True  # Prefer rollup solutions
)

if superseding['resources']:
    print("Using newer rollup solution instead")
    best_solution = superseding['resources'][0]
else:
    best_solution = client.solutions.get_solution(solution_id)
```

### 2. Handle Prerequisites

```python
def get_complete_solution_chain(solution_id: str) -> list:
    """Get solution and all prerequisites in execution order."""
    chain = []
    processed = set()
    
    def add_solution_and_prereqs(sid):
        if sid in processed:
            return
        processed.add(sid)
        
        # Get prerequisites first
        prereqs = client.solutions.get_prerequisites(sid)
        for prereq in prereqs['resources']:
            add_solution_and_prereqs(prereq['id'])
        
        # Add this solution
        solution = client.solutions.get_solution(sid)
        chain.append(solution)
    
    add_solution_and_prereqs(solution_id)
    return chain

# Get ordered solution chain
solutions_to_apply = get_complete_solution_chain('target-solution')
print("Execute in this order:")
for i, sol in enumerate(solutions_to_apply, 1):
    print(f"{i}. {sol['summary']['text']}")
```

### 3. Filter by Solution Type

```python
# Get only patch solutions for automated deployment
patches = client.solutions.get_by_type('patch')

# Get configuration solutions for manual review
configs = client.solutions.get_by_type('configuration')

# Get rollup solutions for comprehensive updates
rollups = client.solutions.get_by_type('rollup')
```

### 4. Error Handling

```python
import requests

try:
    solution = client.solutions.get_solution('solution-id')
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Solution not found")
    else:
        print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Response Examples

### Solution Object

```json
{
  "id": "ubuntu-upgrade-libexpat1",
  "summary": {
    "html": "<p>Upgrade libexpat1</p>",
    "text": "Upgrade libexpat1"
  },
  "steps": {
    "html": "<p>\n    Use `apt-get upgrade` to upgrade libexpat1 to the latest version.\n  </p>",
    "text": "Use `apt-get upgrade` to upgrade libexpat1 to the latest version."
  },
  "additionalInformation": {
    "html": "",
    "text": ""
  },
  "appliesTo": "libexpat1 on Ubuntu Linux",
  "estimate": "PT10M",
  "type": "configuration",
  "links": [
    {
      "href": "https://hostname:3780/api/3/solutions/ubuntu-upgrade-libexpat1",
      "rel": "self"
    }
  ]
}
```

### Solution List Response

```json
{
  "links": [
    {
      "href": "https://hostname:3780/api/3/solutions?page=0&size=10",
      "rel": "self"
    }
  ],
  "page": {
    "number": 0,
    "size": 10,
    "totalPages": 500,
    "totalResources": 5000
  },
  "resources": [
    {
      "id": "solution-1",
      "summary": {
        "html": "<p>Solution summary</p>",
        "text": "Solution summary"
      },
      "type": "patch",
      "appliesTo": "System component",
      "estimate": "PT15M",
      "links": [
        {
          "href": "https://hostname:3780/api/3/solutions/solution-1",
          "rel": "self"
        }
      ]
    }
  ]
}
```

## API Reference

### SolutionsAPI Class Methods

#### `list(page=0, size=500, sort=None)`
List all solutions with pagination.

**Parameters:**
- `page` (int): Page number (zero-based)
- `size` (int): Results per page (max 500)
- `sort` (list): Sort criteria

**Returns:** Dictionary with resources and pagination info

---

#### `get_solution(solution_id)`
Get detailed information for a specific solution.

**Parameters:**
- `solution_id` (str): Solution identifier

**Returns:** Solution dictionary

---

#### `get_prerequisites(solution_id)`
Get prerequisite solutions that must be executed first.

**Parameters:**
- `solution_id` (str): Solution identifier

**Returns:** Dictionary with prerequisite solutions

---

#### `get_superseding_solutions(solution_id, rollup_only=False)`
Get solutions that supersede this solution.

**Parameters:**
- `solution_id` (str): Solution identifier
- `rollup_only` (bool): Return only rollup solutions

**Returns:** Dictionary with superseding solutions

---

#### `get_superseded_solutions(solution_id)`
Get solutions that are superseded by this solution.

**Parameters:**
- `solution_id` (str): Solution identifier

**Returns:** Dictionary with superseded solutions

---

#### `get_all_solutions(sort=None)`
Retrieve all solutions with automatic pagination.

**Parameters:**
- `sort` (list): Sort criteria

**Returns:** List of all solution dictionaries

---

#### `get_by_type(solution_type, page=0, size=500)`
Get solutions filtered by type.

**Parameters:**
- `solution_type` (str): Type ('configuration', 'patch', 'rollup')
- `page` (int): Page number
- `size` (int): Results per page

**Returns:** List of filtered solutions

---

#### `search_by_applies_to(search_term, page=0, size=500)`
Search solutions by what they apply to.

**Parameters:**
- `search_term` (str): Search term for appliesTo field
- `page` (int): Page number
- `size` (int): Results per page

**Returns:** List of matching solutions

---

## Related Documentation

- [Vulnerabilities API](VULNERABILITIES_API.md) - For finding vulnerabilities that need solutions
- [API Standardization](API_STANDARDIZATION.md) - Architecture patterns
- [Examples](EXAMPLES.md) - More code examples

## Support

For issues or questions:
- GitHub Issues: https://github.com/talltechy/insightvm-python/issues
- Rapid7 API Documentation: https://help.rapid7.com/insightvm/en-us/api/
