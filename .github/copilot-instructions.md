# GitHub Copilot Instructions for InsightVM-Python

This document provides guidance for GitHub Copilot when working with the InsightVM-Python repository.

## Project Overview

InsightVM-Python is a modern Python client library for Rapid7 InsightVM and Palo Alto Cortex XDR APIs. The project follows industry-standard patterns with comprehensive type hints and clean, intuitive interfaces.

**Version:** 2.0.0  
**Python Support:** 3.8+  
**Architecture:** BaseAPI inheritance pattern with unified client interface

## Project Structure

```
insightvm-python/
├── src/rapid7/              # Main package
│   ├── __init__.py         # Public API exports
│   ├── auth.py             # Authentication classes (InsightVMAuth, PlatformAuth)
│   ├── client.py           # InsightVMClient (main entry point)
│   ├── config.py           # Configuration management
│   ├── constants.py        # API constants
│   ├── ui.py              # User interface utilities
│   ├── api/               # API modules
│   │   ├── base.py        # BaseAPI foundation class
│   │   ├── assets.py      # Asset operations
│   │   ├── asset_groups.py # Asset group operations
│   │   ├── scans.py       # Scan management
│   │   ├── reports.py     # Report generation
│   │   ├── sites.py       # Site management
│   │   ├── scan_engines.py # Scan engine management
│   │   ├── scan_templates.py # Template management
│   │   └── sonar_queries.py # Sonar integration
│   └── tools/             # Standalone utility scripts
├── src/paloalto/          # Palo Alto Cortex XDR package
├── docs/                  # Documentation
├── tests/                 # Test suite
│   ├── conftest.py       # Shared pytest fixtures
│   ├── test_*.py         # Test modules
│   └── test_rapid7/      # API-specific tests
└── requirements.txt       # Dependencies
```

## Development Setup

### Environment Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with credentials
```

### Required Environment Variables

```bash
INSIGHTVM_API_USERNAME=your_username
INSIGHTVM_API_PASSWORD=your_password
INSIGHTVM_BASE_URL=https://your-console:3780
INSIGHTVM_VERIFY_SSL=false  # For self-signed certificates
```

## Coding Standards

### Python Style Guide

Follow **PEP 8** with these modifications:
- **Line length:** 100 characters (not 79)
- **Imports:** Group by standard library, third-party, local
- **Docstrings:** Google style for all public methods
- **Type hints:** Required for all functions and methods

### Type Hints

All functions **must** include type hints:

```python
from typing import Dict, List, Optional, Any

def list_assets(
    page: int = 0,
    size: int = 500,
    sort: Optional[List[str]] = None
) -> Dict[str, Any]:
    """List assets with pagination."""
    pass
```

### Docstring Format

Use **Google-style docstrings** for all public functions, classes, and methods:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Longer description if needed. Can span multiple
    lines and include details about the function's
    behavior.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param1 is invalid
        TypeError: When param2 is wrong type
        
    Example:
        >>> example_function("test", 42)
        True
    """
    pass
```

### Code Formatting

- **Formatter:** Use `black` for automatic formatting
- **Linter:** Use `flake8` for code quality
- **Type Checker:** Use `mypy` for static type checking

```bash
# Format code
black src/

# Check formatting
black --check src/

# Lint code
flake8 --max-line-length=100 --ignore=E203,W503 src/

# Check types
mypy src/
```

## Architecture Patterns

### BaseAPI Inheritance

All API modules **must** inherit from `BaseAPI`:

```python
from typing import Dict, Any
from .base import BaseAPI

class ExampleAPI(BaseAPI):
    """
    Example API operations.
    
    This class provides methods for managing example resources.
    """
    
    # Define pagination limits
    MAX_PAGE_SIZE = 500
    
    def list(self, page: int = 0, size: int = 500) -> Dict[str, Any]:
        """
        List all resources.
        
        Args:
            page: Page number (0-indexed)
            size: Number of items per page (max 500)
            
        Returns:
            Dict with resources and pagination info
        """
        size = min(size, self.MAX_PAGE_SIZE)
        return self._request('GET', '/examples', params={'page': page, 'size': size})
```

### Unified Client Pattern

All API modules are accessed through the `InsightVMClient`:

```python
# Client initialization
from rapid7 import InsightVMClient

client = InsightVMClient()

# API module access
client.assets.list()         # Asset operations
client.scans.list()          # Scan operations
client.reports.list()        # Report operations
```

### Error Handling

Use appropriate exception handling:

```python
import requests

try:
    result = client.scans.start_site_scan(site_id=123)
except ValueError as e:
    # Configuration errors
    print(f"Configuration error: {e}")
except TimeoutError as e:
    # Timeout errors
    print(f"Operation timed out: {e}")
except requests.exceptions.RequestException as e:
    # API errors
    print(f"API error: {e}")
```

## Testing Requirements

### Test Framework

- **Framework:** pytest
- **Coverage:** pytest-cov
- **Minimum Coverage:** 70%
- **Target Coverage:** 80%

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run verbose
pytest -v

# Skip coverage (faster)
pytest --no-cov
```

### Writing Tests

Create tests following the existing patterns:

```python
# tests/test_example.py
import pytest
from rapid7 import InsightVMClient

class TestExampleAPI:
    """Test suite for Example API."""
    
    def test_list_resources(self, mock_client):
        """Test listing resources."""
        result = mock_client.examples.list(page=0, size=10)
        
        assert 'resources' in result
        assert 'page' in result
        assert len(result['resources']) <= 10
    
    def test_get_resource(self, mock_client):
        """Test getting single resource."""
        result = mock_client.examples.get(resource_id=123)
        
        assert result['id'] == 123
        assert 'name' in result
```

### Test Fixtures

Use shared fixtures from `tests/conftest.py`:

```python
def test_with_mock_auth(mock_auth):
    """Test using mock authentication."""
    # mock_auth fixture provides pre-configured auth
    pass

def test_with_mock_client(mock_client):
    """Test using mock client."""
    # mock_client fixture provides InsightVMClient with mocked responses
    pass
```

## Documentation Standards

### When to Update Documentation

Update documentation when:
- Adding new API modules
- Adding new methods to existing modules
- Changing method signatures
- Adding new features or tools
- Changing configuration options
- Updating dependencies

### Documentation Files

- **README.md:** Project overview, quick start, features
- **CONTRIBUTING.md:** Development guidelines, coding standards
- **docs/API_REFERENCE.md:** Complete API documentation
- **docs/EXAMPLES.md:** Practical code examples
- **docs/[MODULE]_API.md:** Module-specific documentation

### Docstring Requirements

All public functions, classes, and methods **must** have:
- Brief description
- Args section (for parameters)
- Returns section
- Raises section (if applicable)
- Example section (for complex functions)

## Adding New API Modules

### Step-by-Step Process

1. **Create Module File** in `src/rapid7/api/`
2. **Inherit from BaseAPI**
3. **Add to Client** in `src/rapid7/client.py`
4. **Export in __init__.py** in `src/rapid7/api/__init__.py`
5. **Add Tests** in `tests/test_rapid7/`
6. **Update Documentation**

### Example Implementation

```python
# 1. src/rapid7/api/examples.py
from typing import Dict, Any
from .base import BaseAPI

class ExampleAPI(BaseAPI):
    """Example API operations."""
    
    MAX_PAGE_SIZE = 500
    
    def list(self, page: int = 0, size: int = 500) -> Dict[str, Any]:
        """List all examples."""
        size = min(size, self.MAX_PAGE_SIZE)
        return self._request('GET', '/examples', params={'page': page, 'size': size})

# 2. src/rapid7/client.py
from .api.examples import ExampleAPI

class InsightVMClient:
    def __init__(self, ...):
        # ... existing code ...
        self.examples = ExampleAPI(self.auth, verify_ssl, timeout)

# 3. src/rapid7/api/__init__.py
from .examples import ExampleAPI
__all__ = [..., 'ExampleAPI']

# 4. tests/test_rapid7/test_examples.py
def test_list_examples():
    client = InsightVMClient()
    examples = client.examples.list()
    assert 'resources' in examples
```

## CI/CD Workflows

### GitHub Actions

The project uses these workflows:
- **test-coverage.yml:** Run tests and upload coverage to Codacy
- **pylint.yml:** Static code analysis
- **bandit.yml:** Security scanning
- **dependency-review.yml:** Dependency vulnerability checks

### Before Committing

Always run:
```bash
# Format code
black src/

# Run tests
pytest

# Check types
mypy src/

# Lint code
flake8 src/
```

## Git Commit Guidelines

### Branch Naming

- `feature/short-description` - New features
- `bugfix/short-description` - Bug fixes
- `docs/short-description` - Documentation changes
- `refactor/short-description` - Code refactoring

### Commit Messages

Write clear, descriptive commit messages:

```
Short (50 chars or less) summary

More detailed explanatory text, if necessary. Wrap it to
about 72 characters. Use present tense ("Add feature" not
"Added feature").

- Bullet points are okay
- Reference issues: "Fixes #123" or "Relates to #456"
```

## Common Patterns

### Pagination

```python
# Manual pagination
page1 = client.assets.list(page=0, size=500)
page2 = client.assets.list(page=1, size=500)

# Auto-pagination
all_assets = client.assets.get_all(batch_size=500)
```

### SSL Configuration

```python
# Disable SSL verification (self-signed certificates)
client = InsightVMClient(verify_ssl=False)

# Enable SSL verification (default)
client = InsightVMClient(verify_ssl=True)
```

### Context Manager

```python
# Recommended: Use context manager for proper cleanup
with InsightVMClient() as client:
    assets = client.assets.list()
    print(f"Found {len(assets['resources'])} assets")
```

## Important Notes

### Breaking Changes in v2.0

- Replaced manual Base64 encoding with HTTPBasicAuth
- Unified client interface with sub-clients
- Sites API standardized with `SiteManagementTools` for advanced operations
- Scan Engines API methods renamed to avoid conflicts

### Security Considerations

- **Never commit credentials** - Use environment variables
- **Use HTTPS only** - All API communication must be secure
- **SSL verification** - Only disable for self-signed certificates in trusted environments
- **Secret management** - Use `.env` for development, secret management services for production

### Performance Optimization

- Use `MAX_PAGE_SIZE` constants (typically 500)
- Implement auto-pagination for large datasets
- Configure appropriate timeouts
- Use batch operations when available

## Questions or Issues?

If you have questions:
1. Check existing [documentation](docs/)
2. Search [issues](https://github.com/talltechy/insightvm-python/issues)
3. Review [CONTRIBUTING.md](CONTRIBUTING.md)
4. Open a [new issue](https://github.com/talltechy/insightvm-python/issues/new)

## Related Documentation

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Development guidelines
- [README.md](../README.md) - Project overview
- [MIGRATION.md](../MIGRATION.md) - Upgrading from v1.0
- [SECURITY.md](../SECURITY.md) - Security policy
- [docs/API_REFERENCE.md](../docs/API_REFERENCE.md) - Complete API docs
