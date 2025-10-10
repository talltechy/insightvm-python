# InsightVM-Python

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8676b480eff04517b65bc3bfcfeaea9a)](https://app.codacy.com/gh/talltechy/insightvm-python/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

A modern Python client library for Rapid7 InsightVM and Palo Alto Cortex XDR APIs. Built with industry-standard patterns, comprehensive type hints, and a clean, intuitive interface.

## ✨ Features

- **Modern Authentication** - HTTPBasicAuth integration following industry standards
- **Unified Client Interface** - Single entry point with organized sub-clients
- **Comprehensive Asset Management** - Full CRUD operations with auto-pagination
- **Asset Group Operations** - Create, update, delete, and manage dynamic groups
- **Site Management** - Complete site lifecycle management and configuration
- **Scan Operations** - Start, stop, pause, resume, and monitor vulnerability scans
- **Report Management** - Generate, download, and manage security reports
- **Sonar Query Integration** - Query and analyze Sonar data
- **Type-Safe** - Complete type hints throughout the codebase
- **Self-Signed Certificate Support** - Configurable SSL verification for enterprise environments
- **Context Manager Support** - Proper resource cleanup
- **Well Documented** - Comprehensive docstrings and examples

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/talltechy/insightvm-python.git
cd insightvm-python

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root (see `.env.example` for template):

```bash
# Rapid7 InsightVM API
INSIGHTVM_API_USERNAME=your_username
INSIGHTVM_API_PASSWORD=your_password
INSIGHTVM_BASE_URL=https://your-console:3780

# SSL Configuration (optional)
INSIGHTVM_VERIFY_SSL=false  # Set to false for self-signed certificates
```

### Basic Usage

```python
from rapid7 import InsightVMClient

# Create client (loads credentials from environment)
with InsightVMClient() as client:
    # Asset Management
    assets = client.assets.list(page=0, size=100)
    print(f"Found {len(assets['resources'])} assets")
    
    # Scan Operations
    scan_id = client.scans.start_site_scan(
        site_id=123,
        scan_name="Security Audit"
    )
    print(f"Started scan: {scan_id}")
    
    # Report Generation
    content = client.reports.generate_and_download(
        report_id=42,
        timeout=3600
    )
    with open("security_report.pdf.gz", "wb") as f:
        f.write(content)
    
    # Asset Group Management
    group = client.asset_groups.create_high_risk(
        name="Critical Assets",
        threshold=25000
    )
    print(f"Created group: {group['name']}")
```

## 📚 Documentation

### Core Documentation
- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[Usage Examples](docs/EXAMPLES.md)** - Practical code examples
- **[Migration Guide](MIGRATION.md)** - Upgrading from v1.0 to v2.0
- **[Contributing](CONTRIBUTING.md)** - Development guidelines

### API Module Documentation
- **[Scans API](docs/SCANS_API.md)** - Scan management and monitoring
- **[Reports API](docs/REPORTS_API.md)** - Report generation and download
- **[Site Management](docs/SITE_MANAGEMENT.md)** - Site operations and configuration
- **[UI Improvements](docs/UI_IMPROVEMENTS.md)** - User interface enhancements

## 🏗️ Architecture

### Project Structure

```
insightvm-python/
├── src/rapid7/              # Main package
│   ├── auth.py             # Authentication classes
│   ├── client.py           # InsightVMClient
│   ├── config.py           # Configuration management
│   ├── constants.py        # API constants
│   ├── ui.py              # User interface utilities
│   └── api/               # API modules
│       ├── base.py        # BaseAPI foundation
│       ├── assets.py      # Asset operations
│       ├── asset_groups.py # Asset group operations
│       ├── scans.py       # Scan management
│       ├── reports.py     # Report generation
│       ├── sites.py       # Site management
│       └── sonar_queries.py # Sonar integration
├── docs/                  # Documentation
│   ├── API_REFERENCE.md
│   ├── SCANS_API.md
│   ├── REPORTS_API.md
│   └── ...
├── requirements.txt       # Dependencies
├── .env.example          # Configuration template
└── SECURITY.md           # Security policy
```

### Design Patterns

**BaseAPI Inheritance** - All API modules inherit from a common base class:
```python
from rapid7.api.base import BaseAPI

class ScansAPI(BaseAPI):
    MAX_PAGE_SIZE = 500  # Optimization constant
    
    def list(self, page=0, size=500):
        size = min(size, self.MAX_PAGE_SIZE)
        return self._request('GET', 'scans', params={'page': page, 'size': size})
```

**Unified Client** - Single entry point with sub-clients:
```python
client = InsightVMClient()
client.assets.list()         # Asset operations
client.asset_groups.list()   # Asset group operations
client.scans.list()          # Scan operations
client.reports.list()        # Report operations
client.sites.list()          # Site operations
client.sonar_queries.list()  # Sonar operations
```

## 🔧 Advanced Usage

### Custom Configuration

```python
from rapid7 import InsightVMClient

# Explicit credentials
client = InsightVMClient(
    username="admin",
    password="password",
    base_url="https://console:3780",
    verify_ssl=False,
    timeout=(10, 90)  # (connect, read) timeouts
)
```

### Scan Management

```python
# Start a scan for a site
scan_id = client.scans.start_site_scan(
    site_id=123,
    scan_name="Monthly Security Scan",
    scan_template_id="full-audit-without-web-spider"
)

# Monitor scan progress
scan = client.scans.get_scan(scan_id)
print(f"Status: {scan['status']}")
print(f"Progress: {scan.get('tasks', {}).get('pending', 0)} tasks pending")

# Wait for completion
final_scan = client.scans.wait_for_completion(
    scan_id,
    poll_interval=60,
    timeout=7200
)

# Stop a running scan if needed
client.scans.stop_scan(scan_id)
```

### Report Generation

```python
# List available report templates
templates = client.reports.get_templates()
for template in templates['resources']:
    print(f"{template['id']}: {template['name']}")

# Generate and download a report
content = client.reports.generate_and_download(
    report_id=42,
    poll_interval=30,
    timeout=3600
)

# Save the report (usually GZip compressed)
with open("vulnerability_report.pdf.gz", "wb") as f:
    f.write(content)

# Or manage report generation manually
instance_id = client.reports.generate(report_id=42)
client.reports.wait_for_completion(42, instance_id)
report_content = client.reports.download(42, instance_id)
```

### Auto-Pagination

```python
# Get all assets (handles pagination automatically)
all_assets = client.assets.get_all(batch_size=500)
print(f"Total assets: {len(all_assets)}")

# Get all scans across all pages
all_scans = client.scans.get_all_scans()
print(f"Total scans: {len(all_scans)}")

# Get all reports
all_reports = client.reports.get_all_reports()
print(f"Total reports: {len(all_reports)}")
```

### Advanced Search

```python
# Search for high-risk Windows servers
results = client.assets.search({
    "filters": [
        {"field": "risk-score", "operator": "is-greater-than", "value": 20000},
        {"field": "operating-system", "operator": "contains", "value": "Windows Server"}
    ],
    "match": "all"
})

# Filter scans by status
active_scans = client.scans.list(active=True)
```

### Error Handling

```python
import requests

try:
    client = InsightVMClient()
    
    # Start a scan
    scan_id = client.scans.start_site_scan(site_id=123)
    
    # Wait for completion with timeout
    result = client.scans.wait_for_completion(
        scan_id, 
        timeout=3600
    )
    
except ValueError as e:
    print(f"Configuration error: {e}")
except TimeoutError as e:
    print(f"Operation timed out: {e}")
except requests.exceptions.RequestException as e:
    print(f"API error: {e}")
```

## 🔐 Security

### Best Practices

- **No Hardcoded Credentials** - All credentials loaded from environment variables
- **HTTPS Only** - All API communication over secure connections
- **SSL Verification** - Configurable for self-signed certificates (see [SECURITY.md](SECURITY.md))
- **Secret Management** - Use `.env` for development, secret management services for production
- **HTTPBasicAuth** - Industry-standard authentication pattern
- **Timeout Configuration** - Prevent hanging connections

### Security Considerations

⚠️ **Self-Signed Certificates**: When using `verify_ssl=False`, you bypass SSL certificate validation. Only use this in trusted environments with self-signed certificates.

See [SECURITY.md](SECURITY.md) for complete security policy and vulnerability reporting.

## 🧪 Testing

The v2.0 release has been tested against live InsightVM instances:
- ✅ Authentication with HTTPBasicAuth
- ✅ Asset retrieval and management (1182+ assets tested)
- ✅ Asset group creation and management
- ✅ Scan operations (start, stop, pause, resume)
- ✅ Report generation and download
- ✅ Site management operations
- ✅ Self-signed certificate handling
- ✅ Auto-pagination for large datasets

## 📋 Requirements

- Python 3.8+
- requests >= 2.31.0
- python-dotenv >= 1.0.0
- urllib3 >= 2.0.0

## 🔄 Version History

### v2.0.0 (October 2025) - Major Refactoring & Sprint 3
**Core Refactoring:**
- ✅ Replaced manual Base64 encoding with HTTPBasicAuth
- ✅ Unified client interface with sub-clients
- ✅ BaseAPI inheritance pattern for all modules
- ✅ Type hints throughout
- ✅ Context manager support
- ✅ SSL verification configuration

**Sprint 3: Core Operations (COMPLETE - 100%):**
- ✅ **Scans API** - Complete scan lifecycle management (Issue #66, PR #84)
  - Start, stop, pause, resume scans
  - Monitor scan progress and status
  - Site-based and adhoc scanning
  - Scan history and statistics
- ✅ **Reports API** - Full report management (Issue #67, PR #84)
  - Report configuration CRUD
  - Report generation and monitoring
  - Download report content
  - Template and format discovery
- ✅ **Scan Engines API** - Engine and pool management (Issue #68, PR #85)
  - CRUD operations for scan engines
  - Engine pool management
  - Health monitoring and load balancing
  - Site and scan associations
- ✅ **Scan Templates API** - Template management (Issue #69, PR #86)
  - Template CRUD operations
  - Discovery configuration (asset, service, performance)
  - Service discovery settings
  - Performance optimization helpers
- ✅ **Sites API Standardization** (Commit f5980df)
  - Refactored to follow standardized BaseAPI pattern
  - Created `SiteManagementTools` utility class for advanced operations
  - See [SITE_MANAGEMENT.md](docs/SITE_MANAGEMENT.md) for migration guide
- ✅ **Optimization Patterns**
  - MAX_PAGE_SIZE constants for efficient pagination
  - Enhanced timeout validation
  - Type consistency improvements

**Previously Supported:**
- ✅ Comprehensive asset and asset group operations
- ✅ Sonar query integration

**Breaking Changes:**
- ⚠️ **Sites API Standardization**: Custom helper methods moved to `SiteManagementTools`
- ⚠️ See [MIGRATION.md](MIGRATION.md) for complete upgrade guide from v1.0
- ⚠️ See [SITE_MANAGEMENT.md](docs/SITE_MANAGEMENT.md) for Sites API migration details

### v1.0.0 (Previous)
- Initial release with basic functionality

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/issue-XX-description`)
3. Follow the GitHub workflow (issues → branches → PRs)
4. Commit with conventional commit format
5. Push to the branch (`git push origin feature/issue-XX-description`)
6. Open a Pull Request

### Current Sprint Progress

**Sprint 3: Core Operations** ✅ COMPLETE (100%)
- ✅ Issue #66: Scans API Module (COMPLETE - PR #84)
- ✅ Issue #67: Reports API Module (COMPLETE - PR #84)
- ✅ Issue #68: Scan Engines API Module (COMPLETE - PR #85)
- ✅ Issue #69: Scan Templates API Module (COMPLETE - PR #86)
- ✅ Sites API Standardization (COMPLETE - Commit f5980df)

**Sprint 4: Vulnerabilities & Remediation** (NEXT - High Priority)
- ⏳ Issue #70: Vulnerabilities API Module
- ⏳ Issue #71: Solutions API Module
- ⏳ Issue #72: Vulnerability Exceptions API Module

## 📖 API References

- [Official Rapid7 InsightVM API](https://help.rapid7.com/insightvm/en-us/api/index.html)
- [Official Rapid7 InsightVM API Examples](https://github.com/rapid7/insightvm-api-examples)
- [Palo Alto Cortex XDR API](https://docs-cortex.paloaltonetworks.com/r/Cortex-XDR/Cortex-XDR-API-Reference/APIs-Overview)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Rapid7 for the InsightVM API
- The Python requests library maintainers
- Contributors to this project

## 💬 Support

For issues, questions, or contributions, please:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Review the [examples](docs/EXAMPLES.md)
- See [SECURITY.md](SECURITY.md) for security concerns

---

**Note**: This is v2.0 with breaking changes from v1.0. See [MIGRATION.md](MIGRATION.md) for upgrade instructions.
