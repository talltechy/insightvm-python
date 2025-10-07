# InsightVM-Python

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

A modern Python client library for Rapid7 InsightVM and Palo Alto Cortex XDR APIs. Built with industry-standard patterns, comprehensive type hints, and a clean, intuitive interface.

## ✨ Features

- **Modern Authentication** - HTTPBasicAuth integration following industry standards
- **Unified Client Interface** - Single entry point with organized sub-clients
- **Comprehensive Asset Management** - Full CRUD operations with auto-pagination
- **Asset Group Operations** - Create, update, delete, and manage dynamic groups
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
    # List assets
    assets = client.assets.list(page=0, size=100)
    print(f"Found {len(assets['resources'])} assets")
    
    # Get specific asset
    asset = client.assets.get_asset(asset_id=123)
    print(f"Asset: {asset['hostname']}")
    
    # Create high-risk asset group
    group = client.asset_groups.create_high_risk(
        name="Critical Assets",
        threshold=25000
    )
    print(f"Created group: {group['name']}")
```

## 📚 Documentation

- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[Usage Examples](docs/EXAMPLES.md)** - Practical code examples
- **[Migration Guide](MIGRATION.md)** - Upgrading from v1.0 to v2.0
- **[Contributing](CONTRIBUTING.md)** - Development guidelines

## 🏗️ Architecture

### Project Structure

```
insightvm-python/
├── src/rapid7/           # Main package
│   ├── auth.py          # Authentication classes
│   ├── client.py        # InsightVMClient
│   └── api/             # API modules
│       ├── base.py      # BaseAPI foundation
│       ├── assets.py    # Asset operations
│       └── asset_groups.py  # Asset group operations
├── requirements.txt     # Dependencies
├── .env.example        # Configuration template
└── docs/               # Documentation
```

### Design Patterns

**BaseAPI Inheritance** - All API modules inherit from a common base class:
```python
from rapid7.api.base import BaseAPI

class AssetAPI(BaseAPI):
    def list(self, page=0, size=500):
        return self._request('GET', '/assets', params={'page': page, 'size': size})
```

**Unified Client** - Single entry point with sub-clients:
```python
client = InsightVMClient()
client.assets.list()        # Asset operations
client.asset_groups.list()  # Asset group operations
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

### Auto-Pagination

```python
# Get all assets (handles pagination automatically)
all_assets = client.assets.get_all(batch_size=500)
print(f"Total assets: {len(all_assets)}")
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
```

### Error Handling

```python
import requests

try:
    client = InsightVMClient()
    assets = client.assets.get_all()
except ValueError as e:
    print(f"Configuration error: {e}")
except requests.exceptions.RequestException as e:
    print(f"API error: {e}")
```

## 🔐 Security

- **No Hardcoded Credentials** - All credentials loaded from environment variables
- **HTTPS Only** - All API communication over secure connections
- **SSL Verification** - Configurable for self-signed certificates
- **Secret Management** - Use `.env` for development, secret management services for production

## 🧪 Testing

The v2.0 release has been tested against live InsightVM instances:
- ✅ Authentication with HTTPBasicAuth
- ✅ Asset retrieval (1182+ assets)
- ✅ Asset group creation and management
- ✅ Self-signed certificate handling

## 📋 Requirements

- Python 3.8+
- requests >= 2.31.0
- python-dotenv >= 1.0.0
- urllib3 >= 2.0.0

## 🔄 Version History

### v2.0.0 (October 2025) - Major Refactoring
- ✅ Replaced manual Base64 encoding with HTTPBasicAuth
- ✅ Unified client interface with sub-clients
- ✅ BaseAPI inheritance pattern for all modules
- ✅ Comprehensive asset and asset group operations
- ✅ Type hints throughout
- ✅ Context manager support
- ✅ SSL verification configuration
- ⚠️ **Breaking changes** - See [MIGRATION.md](MIGRATION.md) for upgrade guide

### v1.0.0 (Previous)
- Initial release with basic functionality

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

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

---

**Note**: This is v2.0 with breaking changes from v1.0. See [MIGRATION.md](MIGRATION.md) for upgrade instructions.
