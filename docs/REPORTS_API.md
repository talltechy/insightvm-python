# Reports API Documentation

## Overview

The Reports API module provides comprehensive report management functionality for Rapid7 InsightVM, including:

- **Report Configuration Management**: Create, read, update, and delete report configurations
- **Report Generation**: Generate reports on-demand with customizable parameters
- **Report History & Instances**: Track report generation history and manage instances
- **Report Downloads**: Download generated report content (typically GZip compressed)
- **Templates & Formats**: Discover available report templates and output formats
- **Helper Methods**: Convenience methods for common workflows

## Quick Start

```python
from rapid7 import InsightVMClient

# Initialize client
client = InsightVMClient()

# List all reports
reports = client.reports.list()

# Generate a report
instance_id = client.reports.generate(report_id=42)

# Wait for completion and download
instance = client.reports.wait_for_completion(42, str(instance_id))
content = client.reports.download(42, str(instance_id))

# Save to file
with open("report.pdf.gz", "wb") as f:
    f.write(content)
```

## Core Operations

### List Reports

Retrieve all configured reports with pagination:

```python
# Get first page of reports
reports = client.reports.list(page=0, size=100)

for report in reports['resources']:
    print(f"{report['id']}: {report['name']}")
    print(f"  Format: {report['format']}")
    print(f"  Template: {report.get('template', 'N/A')}")
```

### Get Report Details

Retrieve configuration details for a specific report:

```python
report = client.reports.get_report(42)

print(f"Name: {report['name']}")
print(f"Format: {report['format']}")
print(f"Template: {report.get('template')}")
print(f"Owner: {report['owner']}")

# Check scope
scope = report.get('scope', {})
if 'sites' in scope:
    print(f"Sites: {scope['sites']}")
if 'assetGroups' in scope:
    print(f"Asset Groups: {scope['assetGroups']}")
```

### Create Report

Create a new report configuration:

```python
# Basic PDF report for specific sites
config = {
    "name": "Monthly Security Report",
    "format": "pdf",
    "template": "executive-overview",
    "scope": {
        "sites": [42, 43, 44]
    }
}

result = client.reports.create(config)
report_id = result['id']
print(f"Created report ID: {report_id}")

# Advanced configuration with filters and scheduling
advanced_config = {
    "name": "Weekly Vulnerability Report",
    "format": "pdf",
    "template": "audit-report",
    "scope": {
        "assetGroups": [10, 20]
    },
    "filters": {
        "severity": "critical,severe",
        "statuses": ["vulnerable"]
    },
    "frequency": {
        "type": "schedule",
        "start": "2025-01-15T00:00:00Z",
        "repeat": {
            "every": "date-of-month",
            "interval": 1,
            "dayOfWeek": "monday"
        }
    },
    "email": {
        "owner": "file",
        "additionalRecipients": ["security@company.com"]
    }
}

result = client.reports.create(advanced_config)
```

### Update Report

Update an existing report configuration:

```python
# Update report name and scope
updated_config = {
    "name": "Updated Report Name",
    "scope": {
        "sites": [42, 43, 44, 45]  # Added site 45
    }
}

client.reports.update(42, updated_config)
```

### Delete Report

Delete a report configuration:

```python
client.reports.delete_report(42)
```

## Report Generation

### Generate Report

Trigger on-demand report generation:

```python
# Generate report and get instance ID
instance_id = client.reports.generate(42)
print(f"Report generation started: Instance {instance_id}")

# Check status
instance = client.reports.get_instance(42, str(instance_id))
print(f"Status: {instance['status']}")
```

### Wait for Completion

Block until report generation completes:

```python
# Start generation
instance_id = client.reports.generate(42)

# Wait for completion (polls every 30 seconds by default)
final_instance = client.reports.wait_for_completion(
    report_id=42,
    instance_id=str(instance_id),
    poll_interval=60,  # Check every minute
    timeout=3600       # Give up after 1 hour
)

print(f"Report completed: {final_instance['status']}")
print(f"Size: {final_instance['size']['formatted']}")
print(f"Generated: {final_instance['generated']}")
```

### Check Completion Status

Quick check if a report is complete:

```python
if client.reports.is_complete(42, "12345"):
    print("Report is ready for download")
    content = client.reports.download(42, "12345")
else:
    print("Report is still generating...")
```

### Generate and Download

Convenience method that combines generation, waiting, and download:

```python
# One-step generation and download
content = client.reports.generate_and_download(
    report_id=42,
    poll_interval=60,
    timeout=3600
)

# Save to file
with open("security_report.pdf.gz", "wb") as f:
    f.write(content)

# If you need to decompress
import gzip
with gzip.open("security_report.pdf.gz", "rb") as f:
    pdf_content = f.read()
    
with open("security_report.pdf", "wb") as f:
    f.write(pdf_content)
```

## Report History & Instances

### Get Report History

Retrieve all historical generations of a report:

```python
history = client.reports.get_history(42)

print(f"Total instances: {len(history['resources'])}")

for instance in history['resources']:
    print(f"Instance {instance['id']}:")
    print(f"  Status: {instance['status']}")
    print(f"  Generated: {instance['generated']}")
    print(f"  Size: {instance['size']['formatted']}")
```

### Get Specific Instance

Get details for a specific report instance:

```python
instance = client.reports.get_instance(42, "12345")

print(f"Status: {instance['status']}")
print(f"Generated: {instance['generated']}")
print(f"Size: {instance['size']['formatted']}")
print(f"Download URI: {instance.get('uri')}")
```

### Get Latest Instance

Get the most recent report generation:

```python
latest = client.reports.get_latest_instance(42)

if latest:
    print(f"Latest generation: {latest['generated']}")
    print(f"Status: {latest['status']}")
    
    if latest['status'] == 'complete':
        content = client.reports.download(42, str(latest['id']))
else:
    print("No report instances found")
```

### Delete Report Instance

Remove a specific report generation from history:

```python
# Delete old report instance
client.reports.delete_instance(42, "12345")
```

## Download Operations

### Download Report Content

Download the generated report file:

```python
# Download report (usually GZip compressed)
content = client.reports.download(42, "12345")

# Save compressed file
with open("report.pdf.gz", "wb") as f:
    f.write(content)

# Or decompress and save
import gzip
import io

with gzip.GzipFile(fileobj=io.BytesIO(content)) as gz:
    pdf_content = gz.read()
    
with open("report.pdf", "wb") as f:
    f.write(pdf_content)
```

## Templates & Formats

### List Report Templates

Get all available report templates:

```python
templates = client.reports.get_templates()

print("Available Templates:")
for template in templates['resources']:
    print(f"\n{template['id']}: {template['name']}")
    print(f"  Type: {template['type']}")
    print(f"  Built-in: {template['builtin']}")
    print(f"  Description: {template['description']}")
    
    if 'sections' in template:
        print(f"  Sections: {', '.join(template['sections'])}")
```

Common templates include:
- `executive-overview` - High-level summary for executives
- `audit-report` - Comprehensive audit details
- `baseline-comparison` - Compare against baseline
- `pci-attestation` - PCI DSS compliance report
- `hipaa-compliance` - HIPAA compliance report

### Get Template Details

Get details for a specific template:

```python
template = client.reports.get_template("executive-overview")

print(f"Name: {template['name']}")
print(f"Description: {template['description']}")
print(f"Type: {template['type']}")
print(f"Sections: {template.get('sections', [])}")
```

### List Report Formats

Get all available output formats:

```python
formats = client.reports.get_formats()

print("Available Formats:")
for fmt in formats['resources']:
    print(f"\nFormat: {fmt['format']}")
    
    if 'templates' in fmt:
        print(f"  Supported templates: {len(fmt['templates'])}")
        print(f"  Templates: {', '.join(fmt['templates'][:5])}...")
```

Common formats include:
- `pdf` - Adobe PDF
- `html` - HTML document
- `rtf` - Rich Text Format
- `xml` - XML format
- `csv` - Comma-separated values
- `db` - Database format

## Helper Methods

### Get All Reports

Retrieve all reports with automatic pagination:

```python
all_reports = client.reports.get_all_reports()

print(f"Total reports: {len(all_reports)}")

for report in all_reports:
    print(f"{report['id']}: {report['name']}")
```

## Common Use Cases

### Automated Monthly Reporting

Generate and email reports on a schedule:

```python
# Create scheduled monthly report
config = {
    "name": "Monthly Security Summary",
    "format": "pdf",
    "template": "executive-overview",
    "scope": {
        "sites": [42, 43, 44]
    },
    "frequency": {
        "type": "schedule",
        "start": "2025-01-01T09:00:00Z",
        "repeat": {
            "every": "date-of-month",
            "interval": 1  # First of month
        }
    },
    "email": {
        "owner": "file",
        "additionalRecipients": [
            "ciso@company.com",
            "security-team@company.com"
        ],
        "smtp": {
            "global": True
        }
    }
}

result = client.reports.create(config)
print(f"Created scheduled report: {result['id']}")
```

### On-Demand Vulnerability Report

Generate a vulnerability report for specific assets:

```python
# Create report configuration
config = {
    "name": "Critical Vulnerabilities - Production",
    "format": "pdf",
    "template": "audit-report",
    "scope": {
        "assetGroups": [10]  # Production assets
    },
    "filters": {
        "severity": "critical,severe",
        "statuses": ["vulnerable"]
    }
}

# Create and generate immediately
result = client.reports.create(config)
report_id = result['id']

# Generate and download
content = client.reports.generate_and_download(
    report_id=report_id,
    timeout=1800  # 30 minutes
)

# Save report
filename = f"critical_vulns_{report_id}.pdf.gz"
with open(filename, "wb") as f:
    f.write(content)
    
print(f"Report saved: {filename}")
```

### Compliance Reporting

Generate PCI DSS compliance reports:

```python
# PCI compliance report
config = {
    "name": "PCI DSS Quarterly Compliance",
    "format": "pdf",
    "template": "pci-attestation",
    "scope": {
        "assetGroups": [5]  # PCI scope assets
    },
    "filters": {
        "categories": {
            "included": ["PCI"]
        }
    }
}

result = client.reports.create(config)
report_id = result['id']

# Generate report
instance_id = client.reports.generate(report_id)

# Wait and download
instance = client.reports.wait_for_completion(
    report_id,
    str(instance_id),
    timeout=3600
)

content = client.reports.download(report_id, str(instance_id))

with open("pci_compliance.pdf.gz", "wb") as f:
    f.write(content)
```

### Report Cleanup

Clean up old report instances to save space:

```python
import datetime

# Get report history
history = client.reports.get_history(42)

# Delete instances older than 90 days
cutoff = datetime.datetime.now() - datetime.timedelta(days=90)

for instance in history['resources']:
    generated = datetime.datetime.fromisoformat(
        instance['generated'].replace('Z', '+00:00')
    )
    
    if generated < cutoff:
        print(f"Deleting old instance: {instance['id']}")
        client.reports.delete_instance(42, str(instance['id']))
```

## Best Practices

### Report Configuration

1. **Use Descriptive Names**: Make report names clear and specific
   ```python
   # Good
   "Monthly Critical Vulnerabilities - Production Servers"
   
   # Bad
   "Report 1"
   ```

2. **Set Appropriate Scope**: Limit reports to relevant assets
   ```python
   config = {
       "scope": {
           "assetGroups": [10, 20],  # Specific groups
           "tags": [5]                # Or by tags
       }
   }
   ```

3. **Apply Filters**: Reduce noise by filtering results
   ```python
   config = {
       "filters": {
           "severity": "critical,severe",
           "statuses": ["vulnerable"]
       }
   }
   ```

### Report Generation

1. **Use Timeouts**: Always set reasonable timeouts
   ```python
   instance = client.reports.wait_for_completion(
       report_id=42,
       instance_id=str(instance_id),
       timeout=3600  # Don't wait forever
   )
   ```

2. **Handle Errors Gracefully**:
   ```python
   try:
       content = client.reports.generate_and_download(
           report_id=42,
           timeout=1800
       )
   except TimeoutError:
       print("Report generation timed out")
   except RuntimeError as e:
       print(f"Report generation failed: {e}")
   ```

3. **Check Status Before Download**:
   ```python
   if client.reports.is_complete(42, instance_id):
       content = client.reports.download(42, instance_id)
   ```

### Storage Management

1. **Clean Up Old Instances**: Regularly delete old report instances
2. **Decompress When Needed**: Reports are typically GZip compressed
3. **Use Descriptive Filenames**: Include report ID and date

### Scheduling

1. **Use Scheduled Reports**: For recurring needs, use built-in scheduling
2. **Set Appropriate Times**: Schedule during off-peak hours
3. **Configure Email Delivery**: Automate distribution

## Error Handling

### Common Errors

```python
import requests

try:
    # Create report
    result = client.reports.create(config)
    
    # Generate report
    instance_id = client.reports.generate(result['id'])
    
    # Wait for completion
    instance = client.reports.wait_for_completion(
        result['id'],
        str(instance_id),
        timeout=3600
    )
    
    # Download
    content = client.reports.download(result['id'], str(instance_id))
    
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Report not found")
    elif e.response.status_code == 401:
        print("Authentication failed")
    elif e.response.status_code == 400:
        print(f"Bad request: {e.response.text}")
    else:
        print(f"HTTP error: {e}")
        
except TimeoutError as e:
    print(f"Report generation timed out: {e}")
    
except RuntimeError as e:
    print(f"Report generation failed: {e}")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Advanced Features

### Custom Report Queries

For SQL-based reports (database format):

```python
config = {
    "name": "Custom SQL Report",
    "format": "db",
    "query": """
        SELECT 
            a.ip_address,
            a.host_name,
            a.risk_score,
            COUNT(v.vulnerability_id) as vuln_count
        FROM 
            dim_asset a
        LEFT JOIN 
            fact_asset_vulnerability v ON a.asset_id = v.asset_id
        GROUP BY 
            a.asset_id
        HAVING 
            vuln_count > 0
        ORDER BY 
            a.risk_score DESC
    """
}
```

### Baseline Comparison Reports

Compare current state against a baseline:

```python
config = {
    "name": "Baseline Comparison",
    "format": "pdf",
    "template": "baseline-comparison",
    "baseline": {
        "type": "previous_scan",
        "scan_id": 12345
    },
    "scope": {
        "sites": [42]
    }
}
```

### Multi-Site Reporting

Generate reports across multiple sites:

```python
# Get all sites
all_sites = client.sites.get_all_sites()

# Create report for all sites
config = {
    "name": "Enterprise-Wide Vulnerability Report",
    "format": "pdf",
    "template": "executive-overview",
    "scope": {
        "sites": [site['id'] for site in all_sites]
    }
}

result = client.reports.create(config)
```

## API Reference

For complete method signatures and parameters, see the [ReportsAPI class documentation](../src/rapid7/api/reports.py).

### Key Methods

- `list()` - List all report configurations
- `get_report()` - Get report details
- `create()` - Create new report
- `update()` - Update report configuration
- `delete_report()` - Delete report
- `generate()` - Generate report instance
- `get_history()` - Get report generation history
- `get_instance()` - Get instance details
- `delete_instance()` - Delete report instance
- `download()` - Download report content
- `get_templates()` - List available templates
- `get_template()` - Get template details
- `get_formats()` - List available formats
- `wait_for_completion()` - Wait for generation
- `is_complete()` - Check completion status
- `get_latest_instance()` - Get most recent instance
- `get_all_reports()` - Get all reports (paginated)
- `generate_and_download()` - Generate and download

## Related Documentation

- [Scans API Documentation](SCANS_API.md)
- [Site Management Documentation](SITE_MANAGEMENT.md)
- [API Reference](API_REFERENCE.md)
- [Examples](EXAMPLES.md)
