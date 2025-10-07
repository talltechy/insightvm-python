# Contributing to InsightVM-Python

Thank you for your interest in contributing to InsightVM-Python! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Adding New Features](#adding-new-features)

---

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A Rapid7 InsightVM instance for testing (optional but recommended)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/insightvm-python.git
cd insightvm-python
```

3. Add the upstream repository:

```bash
git remote add upstream https://github.com/talltechy/insightvm-python.git
```

---

## Development Setup

### 1. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### 3. Configure Environment

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 4. Verify Setup

```python
from rapid7 import InsightVMClient

client = InsightVMClient()
assets = client.assets.list(page=0, size=1)
print("Setup successful!")
```

---

## Project Structure

```
insightvm-python/
├── src/rapid7/              # Main package
│   ├── __init__.py         # Public API
│   ├── auth.py             # Authentication classes
│   ├── client.py           # InsightVMClient
│   └── api/                # API modules
│       ├── __init__.py     # API package
│       ├── base.py         # BaseAPI foundation
│       ├── assets.py       # Asset operations
│       ├── asset_groups.py # Asset group operations
│       └── sites.py        # Site operations (future)
├── docs/                   # Documentation
├── tests/                  # Test suite (to be added)
├── memory-bank/            # Project knowledge base
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
└── README.md              # Main documentation
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Imports**: Group by standard library, third-party, local
- **Docstrings**: Google style for all public methods

### Type Hints

All functions must include type hints:

```python
from typing import Dict, List, Optional, Any

def list_assets(
    page: int = 0,
    size: int = 500,
    sort: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    List assets with pagination.
    
    Args:
        page: Page number (0-indexed)
        size: Number of assets per page
        sort: Optional sort criteria
        
    Returns:
        Dict with resources and pagination info
        
    Raises:
        ValueError: If size exceeds 500
    """
    pass
```

### Docstring Format

Use Google-style docstrings:

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

Use `black` for automatic formatting:

```bash
# Format all files
black src/

# Check formatting without changes
black --check src/
```

### Linting

Use `flake8` for linting:

```bash
# Run linter
flake8 src/

# With custom config
flake8 --max-line-length=100 --ignore=E203,W503 src/
```

### Type Checking

Use `mypy` for static type checking:

```bash
# Check types
mypy src/
```

---

## Making Changes

### Branch Naming

Use descriptive branch names:

- `feature/short-description` - New features
- `bugfix/short-description` - Bug fixes
- `docs/short-description` - Documentation changes
- `refactor/short-description` - Code refactoring

Examples:
- `feature/site-management`
- `bugfix/pagination-error`
- `docs/api-reference-update`

### Commit Messages

Write clear, descriptive commit messages:

```
Short (50 chars or less) summary

More detailed explanatory text, if necessary. Wrap it to
about 72 characters. The blank line separating the summary
from the body is critical.

- Bullet points are okay
- Use present tense ("Add feature" not "Added feature")
- Reference issues: "Fixes #123" or "Relates to #456"
```

Examples of good commit messages:
```
Add site management module with filtering

Implement SiteAPI class with methods for listing,
filtering, and deleting sites. Includes support for
name patterns and empty site detection.

Fixes #42
```

### Making Changes

1. Create a feature branch:
```bash
git checkout -b feature/my-feature
```

2. Make your changes

3. Test your changes

4. Commit your changes:
```bash
git add .
git commit -m "Add my feature"
```

5. Keep your branch updated:
```bash
git fetch upstream
git rebase upstream/main
```

6. Push to your fork:
```bash
git push origin feature/my-feature
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/rapid7

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Writing Tests

Create test files in the `tests/` directory:

```python
# tests/test_assets.py
import pytest
from rapid7 import InsightVMClient

def test_list_assets():
    """Test asset listing"""
    client = InsightVMClient()
    result = client.assets.list(page=0, size=10)
    
    assert 'resources' in result
    assert 'page' in result
    assert len(result['resources']) <= 10

def test_asset_pagination():
    """Test asset pagination"""
    client = InsightVMClient()
    
    page1 = client.assets.list(page=0, size=5)
    page2 = client.assets.list(page=1, size=5)
    
    assert page1['resources'] != page2['resources']
```

### Test Coverage

Aim for:
- **Minimum**: 70% coverage
- **Target**: 80% coverage
- **Goal**: 90%+ coverage

---

## Submitting Changes

### Pull Request Process

1. **Update Documentation**
   - Update README if needed
   - Add/update docstrings
   - Update CHANGELOG.md

2. **Ensure Tests Pass**
   ```bash
   pytest
   black --check src/
   flake8 src/
   mypy src/
   ```

3. **Create Pull Request**
   - Go to GitHub and create a PR
   - Fill out the PR template
   - Link related issues

4. **PR Description Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   Describe testing performed

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-reviewed code
   - [ ] Commented complex code
   - [ ] Updated documentation
   - [ ] Added tests
   - [ ] Tests pass locally
   - [ ] No new warnings
   ```

5. **Code Review**
   - Address reviewer feedback
   - Make requested changes
   - Re-request review

6. **Merge**
   - Maintainer will merge when approved
   - Branch will be deleted

---

## Adding New Features

### Adding a New API Module

Follow the BaseAPI pattern for consistency:

1. **Create Module File**

```python
# src/rapid7/api/scans.py
from typing import Dict, Any, Optional, List
from .base import BaseAPI

class ScanAPI(BaseAPI):
    """
    Scan operations for InsightVM.
    
    This class provides methods for managing scans including
    starting scans, checking status, and retrieving results.
    """
    
    def list(self) -> Dict[str, Any]:
        """
        List all scans.
        
        Returns:
            Dict with scan list
        """
        return self._request('GET', '/scans')
    
    def get_scan(self, scan_id: int) -> Dict[str, Any]:
        """
        Get details for a specific scan.
        
        Args:
            scan_id: The scan identifier
            
        Returns:
            Dict with scan details
        """
        return self._request('GET', f'/scans/{scan_id}')
    
    def start_scan(self, site_id: int) -> Dict[str, Any]:
        """
        Start a scan for a site.
        
        Args:
            site_id: The site identifier
            
        Returns:
            Dict with scan details
        """
        return self._request('POST', f'/sites/{site_id}/scans')
```

2. **Add to Client**

```python
# src/rapid7/client.py
from .api.scans import ScanAPI

class InsightVMClient:
    def __init__(self, ...):
        # ... existing code ...
        self.scans = ScanAPI(self.auth, verify_ssl, timeout)
```

3. **Export in __init__.py**

```python
# src/rapid7/api/__init__.py
from .scans import ScanAPI

__all__ = ['BaseAPI', 'AssetAPI', 'AssetGroupAPI', 'ScanAPI']
```

4. **Add Tests**

```python
# tests/test_scans.py
def test_list_scans():
    client = InsightVMClient()
    scans = client.scans.list()
    assert 'resources' in scans
```

5. **Update Documentation**

- Add to `docs/API_REFERENCE.md`
- Add examples to `docs/EXAMPLES.md`
- Update README.md features list

### Adding a Convenience Method

```python
def create_high_priority_group(
    self,
    name: str,
    threshold: int = 50000
) -> Dict[str, Any]:
    """
    Create a high-priority asset group.
    
    Convenience method that creates a dynamic asset
    group for assets above a risk threshold.
    
    Args:
        name: Group name
        threshold: Minimum risk score
        
    Returns:
        Created group details
        
    Example:
        >>> group = client.asset_groups.create_high_priority(
        ...     name="Critical Assets",
        ...     threshold=60000
        ... )
    """
    return self.create(
        name=name,
        description=f"Assets with risk score > {threshold}",
        search_criteria={
            "filters": [{
                "field": "risk-score",
                "operator": "is-greater-than",
                "value": threshold
            }],
            "match": "all"
        }
    )
```

---

## Questions?

If you have questions:

1. Check existing [documentation](docs/)
2. Search [issues](https://github.com/talltechy/insightvm-python/issues)
3. Open a [new issue](https://github.com/talltechy/insightvm-python/issues/new)
4. Ask in pull request comments

## Recognition

Contributors will be recognized in:
- Project README
- Release notes
- CHANGELOG.md

Thank you for contributing! 🎉
