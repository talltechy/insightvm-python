# Vulnerabilities API Documentation

## Overview

The Vulnerabilities API module provides comprehensive access to vulnerability data in InsightVM. This includes detailed vulnerability information, CVE/CVSS data, affected assets, exploit information, malware kit associations, and remediation solutions.

**Key Features:**
- List and retrieve vulnerability details
- Access CVE and CVSS scoring information
- Find assets affected by vulnerabilities
- Retrieve exploit and malware kit data
- Get external references and remediation solutions
- Filter by severity, CVSS score, and PCI compliance
- Search by CVE identifier

## Quick Start

```python
from rapid7 import InsightVMClient

# Initialize client
client = InsightVMClient()

# List vulnerabilities
vulns = client.vulnerabilities.list(
    sort=["riskScore,DESC"]
)

# Get vulnerability details
vuln = client.vulnerabilities.get_vulnerability('msft-cve-2017-11804')
print(f"Title: {vuln['title']}")
print(f"Severity: {vuln['severity']}")
print(f"CVSS v3: {vuln['cvss']['v3']['score']}")

# Get affected assets
affected = client.vulnerabilities.get_affected_assets('msft-cve-2017-11804')
print(f"Affected assets: {len(affected['resources'])}")

# Get exploits
exploits = client.vulnerabilities.get_exploits('msft-cve-2017-11804')
print(f"Available exploits: {len(exploits['resources'])}")
```

## Core Operations

### List Vulnerabilities

Retrieve paginated list of all vulnerabilities in the database:

```python
# Basic listing
vulns = client.vulnerabilities.list(page=0, size=500)

# Sort by risk score (highest first)
high_risk = client.vulnerabilities.list(
    sort=["riskScore,DESC"]
)

# Sort by multiple criteria
sorted_vulns = client.vulnerabilities.list(
    sort=["severity,DESC", "riskScore,DESC", "published,DESC"]
)

# Access pagination info
page_info = vulns['page']
print(f"Page {page_info['number']} of {page_info['totalPages']}")
print(f"Total vulnerabilities: {page_info['totalResources']}")
```

### Get Vulnerability Details

Retrieve comprehensive information for a specific vulnerability:

```python
vuln = client.vulnerabilities.get_vulnerability('msft-cve-2017-11804')

# Access basic info
print(f"Title: {vuln['title']}")
print(f"Severity: {vuln['severity']}")
print(f"Risk Score: {vuln['riskScore']}")

# CVSS v3 metrics
cvss_v3 = vuln['cvss']['v3']
print(f"CVSS v3 Score: {cvss_v3['score']}")
print(f"Attack Vector: {cvss_v3['attackVector']}")
print(f"Attack Complexity: {cvss_v3['attackComplexity']}")

# CVSS v2 metrics (if available)
if 'v2' in vuln['cvss']:
    cvss_v2 = vuln['cvss']['v2']
    print(f"CVSS v2 Score: {cvss_v2['score']}")

# CVE identifiers
print(f"CVEs: {', '.join(vuln['cves'])}")

# Categories
print(f"Categories: {', '.join(vuln['categories'])}")

# Description
print(f"Description: {vuln['description']['text']}")

# PCI compliance
pci = vuln['pci']
print(f"PCI Status: {pci['status']}")
print(f"PCI Fail: {pci['fail']}")

# Dates
print(f"Published: {vuln['published']}")
print(f"Modified: {vuln['modified']}")
```

### Find Affected Assets

Get all assets vulnerable to a specific vulnerability:

```python
# Get affected asset IDs
result = client.vulnerabilities.get_affected_assets('ssh-openssh-cve-2023-1234')
asset_ids = result['resources']

print(f"Total affected assets: {len(asset_ids)}")

# Get full asset details for each
for asset_id in asset_ids:
    asset = client.assets.get_asset(asset_id)
    print(f"- {asset['hostName']} ({asset['ip']})")
    print(f"  Risk Score: {asset['riskScore']}")
    print(f"  OS: {asset['os']}")
```

### Get Exploits

Retrieve known exploits for a vulnerability:

```python
# Get all exploits
exploits = client.vulnerabilities.get_exploits('msft-cve-2017-11804')

for exploit in exploits['resources']:
    print(f"\nExploit: {exploit['title']}")
    print(f"  Source: {exploit['source']['name']}")
    print(f"  Skill Level: {exploit['skillLevel']}")
    print(f"  URL: {exploit['source']['link']['href']}")
    
    # Check if it's a Metasploit module
    if exploit['source']['name'] == 'metasploit':
        print(f"  Module: {exploit['source']['key']}")
```

### Get Malware Kits

Retrieve malware kits that exploit a vulnerability:

```python
kits = client.vulnerabilities.get_malware_kits('msft-cve-2017-11804')

for kit in kits['resources']:
    print(f"\nMalware Kit: {kit['name']}")
    print(f"  Popularity: {kit['popularity']}")
    print(f"  ID: {kit['id']}")
```

### Get External References

Access external references like CVE, OSVDB, BID:

```python
refs = client.vulnerabilities.get_references('msft-cve-2017-11804')

for ref in refs['resources']:
    print(f"Source: {ref['source']}")
    print(f"Reference: {ref['reference']}")
    if 'url' in ref:
        print(f"URL: {ref['url']}")
```

### Get Remediation Solutions

Retrieve available solutions:

```python
solutions = client.vulnerabilities.get_solutions('ssh-openssh-cve-2023-1234')

print(f"Available solutions: {len(solutions['resources'])}")

# Get full solution details (requires Solutions API)
for solution_id in solutions['resources']:
    # Would use: solution = client.solutions.get_solution(solution_id)
    print(f"Solution ID: {solution_id}")
```

## Advanced Features

### Retrieve All Vulnerabilities

Use automatic pagination to get complete dataset:

```python
# Warning: This may take time and return 10,000+ vulnerabilities
all_vulns = client.vulnerabilities.get_all_vulnerabilities(
    sort=["riskScore,DESC"]
)

print(f"Total vulnerabilities: {len(all_vulns)}")

# Get top 10 highest risk
top_10 = all_vulns[:10]
for vuln in top_10:
    print(f"{vuln['id']}")
    print(f"  Risk: {vuln['riskScore']}")
    print(f"  Severity: {vuln['severity']}")
```

### Filter by Severity

Get vulnerabilities by severity level:

```python
# Get critical vulnerabilities
critical = client.vulnerabilities.get_by_severity('Critical')
print(f"Critical vulnerabilities: {len(critical)}")

# Get severe vulnerabilities
severe = client.vulnerabilities.get_by_severity('Severe')
print(f"Severe vulnerabilities: {len(severe)}")

# Get moderate vulnerabilities
moderate = client.vulnerabilities.get_by_severity('Moderate')
print(f"Moderate vulnerabilities: {len(moderate)}")

# Convenience method for critical
critical = client.vulnerabilities.get_critical()
```

### Filter by CVSS Score

Get vulnerabilities within CVSS score range:

```python
# Get high CVSS v3 vulnerabilities (7.0-10.0)
high_cvss = client.vulnerabilities.get_by_cvss_score(
    min_score=7.0,
    max_score=10.0,
    cvss_version='v3'
)

# Get medium CVSS v2 vulnerabilities (4.0-6.9)
medium_cvss = client.vulnerabilities.get_by_cvss_score(
    min_score=4.0,
    max_score=6.9,
    cvss_version='v2'
)

print(f"High CVSS v3: {len(high_cvss)}")
print(f"Medium CVSS v2: {len(medium_cvss)}")
```

### Get Exploitable Vulnerabilities

Find vulnerabilities with public exploits:

```python
exploitable = client.vulnerabilities.get_exploitable()

print(f"Exploitable vulnerabilities: {len(exploitable)}")

for vuln in exploitable[:10]:
    print(f"\n{vuln['title']}")
    print(f"  ID: {vuln['id']}")
    print(f"  Risk Score: {vuln['riskScore']}")
    print(f"  CVSS: {vuln['cvss']['v3']['score']}")
    print(f"  Exploits Available: Yes")
```

### Get Vulnerabilities with Malware

Find vulnerabilities actively exploited by malware:

```python
malware_vulns = client.vulnerabilities.get_with_malware()

print(f"Vulnerabilities with malware: {len(malware_vulns)}")

for vuln in malware_vulns[:10]:
    print(f"\n{vuln['title']}")
    print(f"  Risk Score: {vuln['riskScore']}")
    print(f"  Malware Kits: Active")
```

### Get PCI-Failing Vulnerabilities

Find vulnerabilities causing PCI compliance failures:

```python
pci_fails = client.vulnerabilities.get_pci_failing()

print(f"PCI-failing vulnerabilities: {len(pci_fails)}")

for vuln in pci_fails:
    pci = vuln['pci']
    print(f"\n{vuln['title']}")
    print(f"  PCI Status: {pci['status']}")
    print(f"  Adjusted CVSS: {pci['adjustedCVSSScore']}")
    print(f"  Special Notes: {pci.get('specialNotes', 'None')}")
```

### Search by CVE

Find vulnerabilities by CVE identifier:

```python
# Search for specific CVE
results = client.vulnerabilities.search_by_cve('CVE-2017-11804')

for vuln in results:
    print(f"\n{vuln['title']}")
    print(f"  ID: {vuln['id']}")
    print(f"  CVEs: {', '.join(vuln['cves'])}")
    print(f"  Risk Score: {vuln['riskScore']}")
```

## Common Use Cases

### 1. Security Dashboard - Top Vulnerabilities

```python
# Get top 20 highest risk vulnerabilities with exploits
all_vulns = client.vulnerabilities.get_all_vulnerabilities(
    sort=["riskScore,DESC"]
)

# Filter for exploitable only
exploitable = [v for v in all_vulns if v.get('exploits')]
top_20 = exploitable[:20]

print("=" * 80)
print("TOP 20 EXPLOITABLE VULNERABILITIES")
print("=" * 80)

for i, vuln in enumerate(top_20, 1):
    print(f"\n{i}. {vuln['title']}")
    print(f"   ID: {vuln['id']}")
    print(f"   Risk Score: {vuln['riskScore']}")
    print(f"   Severity: {vuln['severity']}")
    print(f"   CVSS v3: {vuln['cvss']['v3']['score']}")
    
    # Get affected assets
    affected = client.vulnerabilities.get_affected_assets(vuln['id'])
    print(f"   Affected Assets: {len(affected['resources'])}")
```

### 2. Vulnerability Remediation Report

```python
# Get critical vulnerabilities with affected assets
critical_vulns = client.vulnerabilities.get_critical()

report_data = []

for vuln in critical_vulns[:50]:  # Top 50
    # Get affected assets
    affected = client.vulnerabilities.get_affected_assets(vuln['id'])
    
    # Get solutions
    solutions = client.vulnerabilities.get_solutions(vuln['id'])
    
    report_data.append({
        'vuln_id': vuln['id'],
        'title': vuln['title'],
        'cvss': vuln['cvss']['v3']['score'],
        'risk_score': vuln['riskScore'],
        'affected_count': len(affected['resources']),
        'solution_count': len(solutions['resources']),
        'cves': vuln['cves']
    })

# Sort by number of affected assets
report_data.sort(key=lambda x: x['affected_count'], reverse=True)

print("\nCRITICAL VULNERABILITY REMEDIATION PRIORITIES")
print("=" * 80)

for item in report_data[:20]:
    print(f"\n{item['title']}")
    print(f"  CVEs: {', '.join(item['cves'][:3])}")  # First 3 CVEs
    print(f"  CVSS: {item['cvss']} | Risk: {item['risk_score']}")
    print(f"  Affected Assets: {item['affected_count']}")
    print(f"  Available Solutions: {item['solution_count']}")
```

### 3. Exploit Intelligence Report

```python
# Get exploitable vulnerabilities
exploitable = client.vulnerabilities.get_exploitable()

exploit_intel = []

for vuln in exploitable[:100]:  # Top 100
    # Get exploit details
    exploits_result = client.vulnerabilities.get_exploits(vuln['id'])
    exploits = exploits_result['resources']
    
    # Check for Metasploit modules
    has_metasploit = any(
        e['source']['name'] == 'metasploit'
        for e in exploits
    )
    
    # Get affected assets
    affected = client.vulnerabilities.get_affected_assets(vuln['id'])
    
    exploit_intel.append({
        'vuln_id': vuln['id'],
        'title': vuln['title'],
        'risk_score': vuln['riskScore'],
        'exploit_count': len(exploits),
        'has_metasploit': has_metasploit,
        'affected_count': len(affected['resources'])
    })

# Sort by risk and exploit availability
exploit_intel.sort(
    key=lambda x: (x['has_metasploit'], x['risk_score']),
    reverse=True
)

print("\nEXPLOIT INTELLIGENCE REPORT")
print("=" * 80)
print(f"Total exploitable vulnerabilities analyzed: {len(exploit_intel)}")

metasploit_count = sum(1 for e in exploit_intel if e['has_metasploit'])
print(f"Vulnerabilities with Metasploit modules: {metasploit_count}")

print("\nTOP EXPLOITABLE THREATS:")
for item in exploit_intel[:15]:
    print(f"\n{item['title']}")
    print(f"  Risk Score: {item['risk_score']}")
    print(f"  Exploits: {item['exploit_count']}")
    if item['has_metasploit']:
        print(f"  ⚠️  METASPLOIT MODULE AVAILABLE")
    print(f"  Affected Assets: {item['affected_count']}")
```

### 4. PCI Compliance Report

```python
# Get all PCI-failing vulnerabilities
pci_fails = client.vulnerabilities.get_pci_failing()

# Categorize by adjusted severity
critical = []
high = []
medium = []

for vuln in pci_fails:
    score = vuln['pci']['adjustedSeverityScore']
    if score >= 4:
        critical.append(vuln)
    elif score == 3:
        high.append(vuln)
    else:
        medium.append(vuln)

print("\nPCI DSS COMPLIANCE REPORT")
print("=" * 80)
print(f"Total PCI-Failing Vulnerabilities: {len(pci_fails)}")
print(f"  Critical (Score 4-5): {len(critical)}")
print(f"  High (Score 3): {len(high)}")
print(f"  Medium (Score 1-2): {len(medium)}")

print("\n\nCRITICAL PCI FAILURES:")
for vuln in critical[:10]:
    pci = vuln['pci']
    print(f"\n{vuln['title']}")
    print(f"  Adjusted CVSS: {pci['adjustedCVSSScore']}")
    print(f"  Severity Score: {pci['adjustedSeverityScore']}")
    
    # Get affected assets
    affected = client.vulnerabilities.get_affected_assets(vuln['id'])
    print(f"  Affected Assets: {len(affected['resources'])}")
```

### 5. CVE Tracking

```python
# Track specific CVEs
cve_list = [
    'CVE-2021-44228',  # Log4Shell
    'CVE-2021-45046',  # Log4Shell variant
    'CVE-2017-5638',   # Apache Struts
    'CVE-2014-0160'    # Heartbleed
]

print("\nCVE TRACKING REPORT")
print("=" * 80)

for cve in cve_list:
    results = client.vulnerabilities.search_by_cve(cve)
    
    print(f"\n{cve}")
    print(f"  Matching vulnerabilities: {len(results)}")
    
    for vuln in results:
        print(f"\n  - {vuln['title']}")
        print(f"    ID: {vuln['id']}")
        print(f"    Risk Score: {vuln['riskScore']}")
        print(f"    CVSS: {vuln['cvss']['v3']['score']}")
        
        # Get affected assets
        affected = client.vulnerabilities.get_affected_assets(vuln['id'])
        print(f"    Affected Assets: {len(affected['resources'])}")
        
        # Check for exploits
        exploits = client.vulnerabilities.get_exploits(vuln['id'])
        if exploits['resources']:
            print(f"    ⚠️  {len(exploits['resources'])} exploit(s) available")
```

## Best Practices

### 1. Use Pagination for Large Datasets

```python
# Instead of get_all_vulnerabilities() for large operations
page = 0
size = 500

while True:
    response = client.vulnerabilities.list(
        page=page,
        size=size,
        sort=["riskScore,DESC"]
    )
    
    vulns = response['resources']
    
    # Process this page
    for vuln in vulns:
        process_vulnerability(vuln)
    
    # Check if done
    page_info = response['page']
    if page_info['number'] >= page_info['totalPages'] - 1:
        break
    
    page += 1
```

### 2. Cache Vulnerability Data

```python
# Cache vulnerability details to avoid repeated API calls
vuln_cache = {}

def get_vulnerability_cached(vuln_id):
    if vuln_id not in vuln_cache:
        vuln_cache[vuln_id] = client.vulnerabilities.get_vulnerability(vuln_id)
    return vuln_cache[vuln_id]

# Use cached data
vuln = get_vulnerability_cached('msft-cve-2017-11804')
```

### 3. Filter Early

```python
# Filter on server side when possible
# For severity filtering, get sorted by risk first
critical = client.vulnerabilities.get_critical()

# Then process only what you need
for vuln in critical[:50]:  # Top 50 only
    # Process vulnerability
    pass
```

### 4. Batch Asset Lookups

```python
# Get affected assets for multiple vulnerabilities efficiently
vuln_ids = ['vuln1', 'vuln2', 'vuln3']

affected_map = {}
for vuln_id in vuln_ids:
    result = client.vulnerabilities.get_affected_assets(vuln_id)
    affected_map[vuln_id] = result['resources']
```

### 5. Error Handling

```python
from requests.exceptions import HTTPError

try:
    vuln = client.vulnerabilities.get_vulnerability('invalid-id')
except HTTPError as e:
    if e.response.status_code == 404:
        print("Vulnerability not found")
    else:
        print(f"API error: {e}")
```

## Response Examples

### Vulnerability Object

```json
{
  "id": "msft-cve-2017-11804",
  "title": "Microsoft CVE-2017-11804: Scripting Engine Memory Corruption Vulnerability",
  "severity": "Severe",
  "severityScore": 4,
  "riskScore": 123.69,
  "cvss": {
    "v2": {
      "accessComplexity": "M",
      "accessVector": "L",
      "authentication": "N",
      "availabilityImpact": "P",
      "confidentialityImpact": "P",
      "integrityImpact": "P",
      "exploitScore": 3.3926,
      "impactScore": 6.443,
      "score": 4.4,
      "vector": "AV:L/AC:M/Au:N/C:P/I:P/A:P"
    },
    "v3": {
      "attackComplexity": "H",
      "attackVector": "N",
      "availabilityImpact": "H",
      "confidentialityImpact": "H",
      "integrityImpact": "H",
      "privilegeRequired": "N",
      "scope": "U",
      "score": 7.5,
      "userInteraction": "R",
      "exploitScore": 1.6201,
      "impactScore": 5.8731,
      "vector": "CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H"
    }
  },
  "cves": ["CVE-2017-11804"],
  "categories": ["Microsoft Windows", "Remote Execution"],
  "description": {
    "html": "<p>A remote code execution vulnerability exists...</p>",
    "text": "A remote code execution vulnerability exists..."
  },
  "published": "2017-10-10",
  "added": "2017-10-10",
  "modified": "2017-10-10",
  "pci": {
    "adjustedCVSSScore": 4,
    "adjustedSeverityScore": 3,
    "fail": true,
    "status": "Fail",
    "specialNotes": ""
  },
  "denialOfService": false,
  "exploits": 2,
  "malwareKits": 1
}
```

### Exploit Object

```json
{
  "id": 4924,
  "title": "Microsoft IIS WebDav ScStoragePathFromUrl Overflow",
  "skillLevel": "expert",
  "source": {
    "name": "metasploit",
    "key": "exploit/windows/iis/iis_webdav_scstoragepathfromurl",
    "link": {
      "href": "http://www.metasploit.com/modules/exploit/windows/iis/iis_webdav_scstoragepathfromurl",
      "rel": "Source"
    }
  }
}
```

### Malware Kit Object

```json
{
  "id": 152,
  "name": "Alpha Pack",
  "popularity": "Rare"
}
```

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/3/vulnerabilities` | List all vulnerabilities |
| GET | `/api/3/vulnerabilities/{id}` | Get vulnerability details |
| GET | `/api/3/vulnerabilities/{id}/assets` | Get affected assets |
| GET | `/api/3/vulnerabilities/{id}/exploits` | Get exploits |
| GET | `/api/3/vulnerabilities/{id}/malware_kits` | Get malware kits |
| GET | `/api/3/vulnerabilities/{id}/references` | Get external references |
| GET | `/api/3/vulnerabilities/{id}/solutions` | Get solutions |

## Related Documentation

- [Assets API](ASSET_MANAGEMENT.md) - For working with affected assets
- [Scans API](SCANS_API.md) - For scanning assets for vulnerabilities
- [Reports API](REPORTS_API.md) - For generating vulnerability reports
- [API Standardization](API_STANDARDIZATION.md) - For understanding API patterns
