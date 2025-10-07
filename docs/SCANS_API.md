# Scans API Documentation

The Scans API module provides comprehensive functionality for managing vulnerability scans in InsightVM, including starting scans, monitoring progress, and controlling scan execution.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Core Operations](#core-operations)
- [Scan Control](#scan-control)
- [Monitoring and Status](#monitoring-and-status)
- [Helper Methods](#helper-methods)
- [Common Use Cases](#common-use-cases)
- [Best Practices](#best-practices)

## Overview

The `ScansAPI` class provides methods for:
- Listing and retrieving scans with pagination
- Starting scans for sites with customizable options
- Controlling scan execution (stop, pause, resume)
- Monitoring scan status and progress
- Retrieving scan history and results
- Automatic pagination for bulk operations

All operations follow the v2.0 BaseAPI pattern with proper authentication, error handling, and type hints.

## Quick Start

```python
from rapid7 import InsightVMClient

# Create client
client = InsightVMClient()

# List all scans
scans = client.scans.list()
print(f"Found {len(scans['resources'])} scans")

# Start a scan
scan_id = client.scans.start_site_scan(
    site_id=42,
    scan_name="Weekly Security Audit"
)
print(f"Started scan {scan_id}")

# Monitor scan status
scan = client.scans.get_scan(scan_id)
print(f"Status: {scan['status']}")
```

## Core Operations

### List All Scans

Retrieve a paginated list of scans with optional filtering:

```python
# Get all scans (paginated)
scans = client.scans.list(page=0, size=100)

# Get only active (running) scans
active_scans = client.scans.list(active=True)

# Get completed scans sorted by end time
completed = client.scans.list(
    active=False,
    sort=["endTime,DESC"]
)

# Custom pagination
scans = client.scans.list(
    page=2,
    size=50,
    sort=["startTime,DESC"]
)
```

### Get Scan Details

Retrieve comprehensive information about a specific scan:

```python
# Get scan by ID
scan = client.scans.get_scan(12345)

# Access scan properties
print(f"Name: {scan['scanName']}")
print(f"Status: {scan['status']}")
print(f"Assets: {scan['assets']}")
print(f"Duration: {scan['duration']}")

# Vulnerability counts
vulns = scan['vulnerabilities']
print(f"Critical: {vulns['critical']}")
print(f"Severe: {vulns['severe']}")
print(f"Total: {vulns['total']}")
```

### Get Site Scans

Retrieve all scans for a specific site:

```python
# Get all scans for a site
site_scans = client.scans.get_site_scans(site_id=42)

# Get only active scans for site
active = client.scans.get_site_scans(
    site_id=42,
    active=True
)

# Get paginated site scans
scans = client.scans.get_site_scans(
    site_id=42,
    page=0,
    size=50,
    sort=["startTime,DESC"]
)
```

### Start Site Scan

Initiate a new scan with various configuration options:

```python
# Basic scan with defaults
scan_id = client.scans.start_site_scan(site_id=42)

# Customized scan
scan_id = client.scans.start_site_scan(
    site_id=42,
    scan_name="Monthly Security Audit",
    scan_template_id="full-audit-without-web-spider",
    hosts=["192.168.1.10", "192.168.1.20"],
    override_blackout=True
)

# Scan with specific engine
scan_id = client.scans.start_site_scan(
    site_id=42,
    engine_id=5,
    scan_name="Datacenter Scan"
)

# Scan with asset groups
scan_id = client.scans.start_site_scan(
    site_id=42,
    asset_group_ids=[10, 11, 12],
    scan_template_id="discovery"
)
```

#### Common Scan Templates

- `full-audit-without-web-spider` - Comprehensive scan without web app testing
- `full-audit` - Complete vulnerability assessment including web apps
- `discovery` - Quick discovery scan
- `exhaustive` - Thorough scan with all checks enabled

## Scan Control

### Stop Scan

Stop a running or paused scan:

```python
# Stop a scan
result = client.scans.stop_scan(scan_id=12345)

# Verify stopped
scan = client.scans.get_scan(12345)
if scan['status'] == 'stopped':
    print("Scan stopped successfully")
```

### Pause Scan

Temporarily pause a running scan:

```python
# Pause a scan
result = client.scans.pause_scan(scan_id=12345)

# Check status
scan = client.scans.get_scan(12345)
print(f"Status: {scan['status']}")  # Should be 'paused'
```

### Resume Scan

Resume a paused scan:

```python
# Resume a paused scan
result = client.scans.resume_scan(scan_id=12345)

# Verify resumed
scan = client.scans.get_scan(12345)
if scan['status'] == 'running':
    print("Scan resumed successfully")
```

## Monitoring and Status

### Check Scan Status

```python
# Check if scan is running
if client.scans.is_scan_running(12345):
    print("Scan is still in progress")
else:
    print("Scan has completed")

# Get detailed status
scan = client.scans.get_scan(12345)
print(f"Status: {scan['status']}")
print(f"Message: {scan['message']}")
```

### Wait for Completion

Block until a scan completes:

```python
# Start scan and wait for completion
scan_id = client.scans.start_site_scan(site_id=42)

# Wait indefinitely
final_scan = client.scans.wait_for_scan_completion(scan_id)
print(f"Scan completed: {final_scan['status']}")

# Wait with timeout (2 hours)
try:
    final_scan = client.scans.wait_for_scan_completion(
        scan_id=scan_id,
        poll_interval=60,  # Check every 60 seconds
        timeout=7200  # 2 hours max
    )
    print(f"Scan finished: {final_scan['endTime']}")
except TimeoutError:
    print("Scan did not complete within 2 hours")
```

### Get Scan Summary

Retrieve key metrics in a simplified format:

```python
# Get scan summary
summary = client.scans.get_scan_summary(12345)

print(f"Name: {summary['name']}")
print(f"Status: {summary['status']}")
print(f"Assets Scanned: {summary['assets_scanned']}")
print(f"Duration: {summary['duration']}")

# Vulnerability breakdown
vulns = summary['vulnerabilities']
print(f"Critical: {vulns['critical']}")
print(f"Severe: {vulns['severe']}")
print(f"Moderate: {vulns['moderate']}")
print(f"Total: {vulns['total']}")
```

## Helper Methods

### Get All Scans (Auto-Pagination)

Retrieve all scans automatically handling pagination:

```python
# Get all scans
all_scans = client.scans.get_all_scans()
print(f"Total scans: {len(all_scans)}")

# Get all active scans
active_scans = client.scans.get_all_scans(active=True)

# Get all completed scans sorted
completed = client.scans.get_all_scans(
    active=False,
    sort=["endTime,DESC"]
)
```

### Get Active Scans

Convenience method for currently running scans:

```python
# Get all active scans
active = client.scans.get_active_scans()

print(f"Currently running: {len(active)} scans")
for scan in active:
    print(f"- {scan['scanName']}: {scan['assets']} assets scanned")
```

### Get Completed Scans

Convenience method for completed scans:

```python
# Get recent completed scans
completed = client.scans.get_completed_scans(
    sort=["endTime,DESC"]
)

print(f"Last 5 completed scans:")
for scan in completed[:5]:
    print(f"- {scan['scanName']}: {scan['endTime']}")
```

## Common Use Cases

### Scheduled Scanning Workflow

```python
from rapid7 import InsightVMClient
from datetime import datetime

# Weekly security audit workflow
def run_weekly_audit():
    client = InsightVMClient()
    
    # Start scan
    scan_id = client.scans.start_site_scan(
        site_id=42,
        scan_name=f"Weekly Audit {datetime.now().strftime('%Y-%m-%d')}",
        scan_template_id="full-audit-without-web-spider"
    )
    
    print(f"Started scan {scan_id}")
    
    # Wait for completion
    final_scan = client.scans.wait_for_scan_completion(
        scan_id=scan_id,
        poll_interval=300,  # Check every 5 minutes
        timeout=28800  # 8 hour max
    )
    
    # Get summary
    summary = client.scans.get_scan_summary(scan_id)
    
    # Report results
    print(f"Scan completed in {summary['duration']}")
    print(f"Found {summary['vulnerabilities']['critical']} critical vulnerabilities")
    
    return summary

# Run the audit
results = run_weekly_audit()
```

### Monitor Multiple Scans

```python
# Monitor all active scans
def monitor_active_scans():
    active = client.scans.get_active_scans()
    
    if not active:
        print("No scans currently running")
        return
    
    print(f"Monitoring {len(active)} active scans:")
    for scan in active:
        summary = client.scans.get_scan_summary(scan['id'])
        print(f"\n{summary['name']}:")
        print(f"  Status: {summary['status']}")
        print(f"  Assets: {summary['assets_scanned']}")
        print(f"  Engine: {summary['engine_name']}")
        print(f"  Started: {summary['start_time']}")

monitor_active_scans()
```

### Scan History Analysis

```python
# Analyze scan history for a site
def analyze_scan_history(site_id, days=30):
    # Get recent scans
    scans = client.scans.get_site_scans(
        site_id=site_id,
        active=False,
        sort=["endTime,DESC"],
        size=100
    )
    
    # Analyze results
    total_scans = len(scans['resources'])
    total_assets = sum(s['assets'] for s in scans['resources'])
    
    print(f"Scan History for Site {site_id} (last {days} days):")
    print(f"Total scans: {total_scans}")
    print(f"Total assets scanned: {total_assets}")
    
    # Show recent scan durations
    if scans['resources']:
        print("\nRecent scan durations:")
        for scan in scans['resources'][:5]:
            duration = scan.get('duration', 'N/A')
            print(f"- {scan['scanName']}: {duration}")

analyze_scan_history(site_id=42)
```

### Emergency Scan Stop

```python
# Stop all running scans (emergency)
def emergency_stop_all():
    active = client.scans.get_active_scans()
    
    print(f"Stopping {len(active)} active scans...")
    
    stopped = []
    failed = []
    
    for scan in active:
        try:
            client.scans.stop_scan(scan['id'])
            stopped.append(scan['scanName'])
        except Exception as e:
            failed.append((scan['scanName'], str(e)))
    
    print(f"\nStopped: {len(stopped)} scans")
    print(f"Failed: {len(failed)} scans")
    
    if failed:
        print("\nFailed scans:")
        for name, error in failed:
            print(f"- {name}: {error}")

# Use with caution!
# emergency_stop_all()
```

## Best Practices

### 1. Monitor Long-Running Scans

```python
# Always set timeouts for long operations
final_scan = client.scans.wait_for_scan_completion(
    scan_id=scan_id,
    poll_interval=300,  # Don't poll too frequently
    timeout=28800  # Set reasonable timeout
)
```

### 2. Handle Scan Failures

```python
# Check scan status after completion
final_scan = client.scans.wait_for_scan_completion(scan_id)

if final_scan['status'] == 'error':
    print(f"Scan failed: {final_scan['message']}")
    # Handle error appropriately
elif final_scan['status'] == 'stopped':
    print("Scan was stopped before completion")
else:
    print("Scan completed successfully")
```

### 3. Use Appropriate Templates

```python
# Choose template based on requirements
templates = {
    'quick_discovery': 'discovery',  # Fast, minimal checks
    'standard_audit': 'full-audit-without-web-spider',  # Recommended
    'comprehensive': 'full-audit',  # Includes web app testing
    'thorough': 'exhaustive'  # Most complete, longest
}

scan_id = client.scans.start_site_scan(
    site_id=42,
    scan_template_id=templates['standard_audit']
)
```

### 4. Respect Blackout Windows

```python
# Only override blackout when necessary
scan_id = client.scans.start_site_scan(
    site_id=42,
    override_blackout=False  # Respect configured windows
)
```

### 5. Monitor Resource Usage

```python
# Check active scans before starting new ones
active = client.scans.get_active_scans()

if len(active) >= 5:
    print("Too many concurrent scans, waiting...")
    # Implement queuing or wait logic
else:
    scan_id = client.scans.start_site_scan(site_id=42)
```

### 6. Log Scan Results

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log scan lifecycle
scan_id = client.scans.start_site_scan(site_id=42)
logger.info(f"Started scan {scan_id} for site 42")

final_scan = client.scans.wait_for_scan_completion(scan_id)
summary = client.scans.get_scan_summary(scan_id)

logger.info(
    f"Scan {scan_id} completed: "
    f"{summary['vulnerabilities']['total']} vulnerabilities found"
)
```

## Error Handling

```python
import requests

try:
    scan_id = client.scans.start_site_scan(site_id=42)
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Site not found")
    elif e.response.status_code == 401:
        print("Authentication failed")
    elif e.response.status_code == 503:
        print("Service unavailable, try again later")
    else:
        print(f"HTTP error: {e}")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Advanced Features

### Custom Scan Configuration

```python
# Highly customized scan
scan_id = client.scans.start_site_scan(
    site_id=42,
    scan_name="Custom Scan",
    scan_template_id="full-audit-without-web-spider",
    hosts=[
        "10.0.1.0/24",  # Subnet
        "192.168.1.100",  # Single host
        "server*.example.com"  # Hostname pattern
    ],
    asset_group_ids=[5, 6, 7],  # Include specific asset groups
    engine_id=3,  # Use specific scan engine
    override_blackout=True  # Override blackout windows
)
```

### Scan Status Polling

```python
import time

def poll_scan_status(scan_id, interval=30):
    """Poll scan status until completion."""
    while True:
        scan = client.scans.get_scan(scan_id)
        status = scan['status']
        
        if status in ['finished', 'stopped', 'error']:
            return scan
        
        print(f"Status: {status}, Assets: {scan['assets']}")
        time.sleep(interval)

# Use the poller
final_scan = poll_scan_status(scan_id, interval=60)
```

## API Reference

For complete API documentation, see the inline docstrings in `src/rapid7/api/scans.py`.

Key methods:
- `list()` - List scans with pagination
- `get_scan()` - Get scan details
- `get_site_scans()` - Get scans for a site
- `start_site_scan()` - Start a new scan
- `stop_scan()` - Stop a scan
- `pause_scan()` - Pause a scan
- `resume_scan()` - Resume a scan
- `wait_for_scan_completion()` - Wait for scan to finish
- `get_scan_summary()` - Get scan summary
- `is_scan_running()` - Check if scan is running
- `get_active_scans()` - Get all active scans
- `get_completed_scans()` - Get all completed scans
- `get_all_scans()` - Get all scans with auto-pagination
