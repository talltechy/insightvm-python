# API Module Standardization (October 2025)

## Overview

This document describes the standardization work done to ensure consistency across all InsightVM-Python API modules, particularly focusing on the integration of recently merged Scans and Reports API modules.

## Problem Identified

When reviewing recently merged changes (Scans API and Reports API modules), we identified critical inconsistencies in how different API modules were calling the BaseAPI:

### Before Standardization

**Old Pattern (Assets, Sites, Asset Groups):**
```python
# Uses helper methods and manually parses JSON
response = self.get('assets', params=params)
return response.json()  # Manual .json() call
```

**New Pattern (Scans, Reports):**
```python
# Uses _request() directly, expects JSON back
return self._request('GET', 'scans', params=params)
# Expected to return Dict[str, Any] but was returning Response object
```

**BaseAPI._request() Behavior:**
- Originally returned `requests.Response` objects
- New modules expected it to return parsed JSON dictionaries
- This mismatch meant the new modules were **broken**

## Solution Implemented

### 1. Enhanced BaseAPI._request()

Updated `_request()` to automatically parse JSON by default:

```python
def _request(
    self,
    method: str,
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    return_raw: bool = False,  # NEW parameter
    **kwargs
) -> Any:
    """
    Make an API request with automatic JSON parsing.
    
    By default, returns parsed JSON dictionaries.
    For binary content (downloads), use return_raw=True.
    """
    # ... request logic ...
    
    if return_raw:
        return response  # Raw Response object
    
    return response.json()  # Parsed JSON (default)
```

**Key Changes:**
- **Default behavior**: Returns parsed JSON dictionaries
- **New parameter `return_raw`**: When True, returns raw Response object
- **Use case for `return_raw=True`**: Binary downloads (PDF, files, etc.)

### 2. Maintained Backward Compatibility

Updated helper methods to maintain compatibility with existing code:

```python
def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
    """Returns raw Response for backward compatibility."""
    return self._request('GET', endpoint, params=params, return_raw=True, **kwargs)
```

All helper methods (`get`, `post`, `put`, `delete`) now pass `return_raw=True` to maintain backward compatibility with existing modules.

## Standardized Patterns

### Pattern 1: Modern _request() Usage (RECOMMENDED)

**For JSON responses:**
```python
def list(self, page: int = 0, size: int = 500) -> Dict[str, Any]:
    """List resources with automatic JSON parsing."""
    params = {'page': page, 'size': size}
    return self._request('GET', 'scans', params=params)
    # Returns parsed JSON dictionary directly
```

**For binary content (downloads):**
```python
def download(self, report_id: int, instance_id: str) -> bytes:
    """Download report content."""
    response = self._request(
        'GET',
        f'reports/{report_id}/history/{instance_id}/output',
        return_raw=True  # Get raw Response for binary content
    )
    return response.content
```

### Pattern 2: Legacy Helper Methods (BACKWARD COMPATIBLE)

```python
def list(self, page: int = 0, size: int = 500) -> Dict[str, Any]:
    """List resources using legacy pattern."""
    params = {'page': page, 'size': size}
    response = self.get('assets', params=params)  # Returns Response
    return response.json()  # Manual JSON parsing
```

## Module Status

### ✅ Standardized Modules (Using Modern Pattern)

These modules use `_request()` directly and benefit from automatic JSON parsing:

1. **ScansAPI** (`src/rapid7/api/scans.py`)
   - All methods use `_request()` directly
   - Returns parsed JSON dictionaries
   - Fully compatible with new standardization

2. **ReportsAPI** (`src/rapid7/api/reports.py`)
   - Most methods use `_request()` directly
   - `download()` method correctly uses `return_raw=True` for binary content
   - Fully compatible with new standardization

### ⚠️ Legacy Modules (Using Old Pattern - Still Works)

These modules use helper methods and manual `.json()` calls:

1. **AssetAPI** (`src/rapid7/api/assets.py`)
   - Uses `self.get()`, `self.post()`, etc.
   - Manually calls `.json()` on responses
   - **Works correctly** due to backward compatibility
   - **Should be migrated** to modern pattern eventually

2. **SiteAPI** (`src/rapid7/api/sites.py`)
   - Uses `self.get()`, `self.post()`, etc.
   - Manually calls `.json()` on responses
   - **Works correctly** due to backward compatibility
   - **Should be migrated** to modern pattern eventually

3. **AssetGroupAPI** (`src/rapid7/api/asset_groups.py`)
   - Uses `self.get()`, `self.post()`, etc.
   - Manually calls `.json()` on responses
   - **Works correctly** due to backward compatibility
   - **Should be migrated** to modern pattern eventually

4. **SonarQueryAPI** (`src/rapid7/api/sonar_queries.py`)
   - Status: Needs review
   - **Should be migrated** to modern pattern eventually

## Migration Guide

### For New API Modules

When creating new API modules, use the modern pattern:

```python
class NewAPI(BaseAPI):
    """New API module."""
    
    def list(self, page: int = 0, size: int = 500) -> Dict[str, Any]:
        """List resources."""
        params = {'page': page, 'size': size}
        # Direct _request() usage - returns JSON automatically
        return self._request('GET', 'resource', params=params)
    
    def get(self, resource_id: int) -> Dict[str, Any]:
        """Get single resource."""
        return self._request('GET', f'resource/{resource_id}')
    
    def download(self, resource_id: int) -> bytes:
        """Download binary content."""
        response = self._request(
            'GET',
            f'resource/{resource_id}/download',
            return_raw=True  # For binary content
        )
        return response.content
```

### For Existing Legacy Modules

Legacy modules will continue to work without changes. To migrate to the modern pattern:

**Before:**
```python
def list(self, page: int = 0, size: int = 500) -> Dict[str, Any]:
    params = {'page': page, 'size': size}
    response = self.get('assets', params=params)
    return response.json()
```

**After:**
```python
def list(self, page: int = 0, size: int = 500) -> Dict[str, Any]:
    params = {'page': page, 'size': size}
    return self._request('GET', 'assets', params=params)
```

## Benefits of Standardization

1. **Consistency**: All new modules follow the same pattern
2. **Simplicity**: No need for manual `.json()` calls
3. **Type Safety**: Methods return `Dict[str, Any]` as declared
4. **Clarity**: Intent is clearer with `return_raw=True` for binary content
5. **Backward Compatible**: Existing code continues to work
6. **Future-Proof**: Easy to add new features to `_request()`

## Testing Recommendations

After migrating a module to the modern pattern:

1. **Verify JSON responses**: Ensure methods return dictionaries, not Response objects
2. **Test binary downloads**: Confirm `return_raw=True` works for file downloads
3. **Check error handling**: Verify HTTPError exceptions are raised correctly
4. **Validate pagination**: Test automatic pagination with `get_all()` methods

## Future Work

### Recommended Migrations (Low Priority)

These migrations are **optional** since backward compatibility is maintained:

- [ ] Migrate AssetAPI to modern pattern
- [ ] Migrate SiteAPI to modern pattern
- [ ] Migrate AssetGroupAPI to modern pattern
- [ ] Migrate SonarQueryAPI to modern pattern

### Considerations

- **No breaking changes**: Migrations are optional improvements
- **Testing required**: Each migration should be tested
- **Documentation**: Update module docstrings to reflect modern pattern
- **Low priority**: Focus on new features first

## Summary

The standardization ensures:
- **New modules** (Scans, Reports) work correctly with automatic JSON parsing
- **Old modules** (Assets, Sites, etc.) continue to work via backward compatibility
- **Consistent patterns** for all future API module development
- **Clear migration path** for eventually standardizing all modules

All modules now work correctly, and we have a clear, documented pattern for future development.
