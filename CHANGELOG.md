# Changelog

All notable changes to InsightVM-Python will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-07

### 🎉 Major Release - Complete Architecture Refactoring

This is a **major breaking release** with significant improvements to the codebase. v2.0 is not backward compatible with v1.0. See [MIGRATION.md](MIGRATION.md) for upgrade instructions.

### Added

#### Authentication
- ✨ Modern authentication using `requests.auth.HTTPBasicAuth` (industry standard)
- ✨ `InsightVMAuth` class for unified authentication
- ✨ `PlatformAuth` class for Rapid7 Platform API
- ✨ Environment variable support with `python-dotenv`
- ✨ SSL verification configuration via `INSIGHTVM_VERIFY_SSL` environment variable
- ✨ Automatic credential validation on initialization

#### API Architecture
- ✨ `InsightVMClient` - Unified client with sub-clients pattern
- ✨ `BaseAPI` - Foundation class for all API modules (inheritance pattern)
- ✨ Context manager support for automatic cleanup
- ✨ Factory function `create_client()` for convenience
- ✨ Consistent error handling across all modules
- ✨ Configurable timeouts (connection and read)

#### Asset Operations
- ✨ `AssetAPI` class with comprehensive operations:
  - `list()` - List assets with pagination
  - `get_asset()` - Get individual asset details
  - `search()` - Advanced search with criteria
  - `get_all()` - Auto-pagination for bulk retrieval
  - `get_vulnerabilities()` - Asset vulnerability data
  - `get_software()` - Software inventory
  - `get_services()` - Service information
  - `get_tags()` / `add_tag()` / `remove_tag()` - Tag management

#### Asset Group Operations
- ✨ `AssetGroupAPI` class with full CRUD:
  - `list()` - List all asset groups
  - `get_group()` - Get group details
  - `create()` - Create new asset group
  - `create_high_risk()` - Convenience method for high-risk groups
  - `update()` - Update group properties
  - `delete_group()` - Delete asset group
  - `get_assets()` - Get group members
  - `add_asset()` / `remove_asset()` - Manage members
  - `get_tags()` / `add_tag()` / `remove_tag()` - Tag operations
  - `search()` - Search asset groups

#### Documentation
- ✨ Comprehensive README with quick start guide
- ✨ Migration guide (MIGRATION.md) for v1.0 users
- ✨ Complete API reference (docs/API_REFERENCE.md)
- ✨ Practical usage examples (docs/EXAMPLES.md)
- ✨ Contributing guidelines (CONTRIBUTING.md)
- ✨ Environment configuration template (.env.example)
- ✨ Memory bank for project knowledge preservation

#### Developer Experience
- ✨ Complete type hints throughout codebase
- ✨ Google-style docstrings for all public methods
- ✨ Clear import paths (`from rapid7 import InsightVMClient`)
- ✨ Standardized environment variable naming (`INSIGHTVM_*` prefix)
- ✨ requirements.txt for dependency management

### Changed

#### Breaking Changes
- 🔥 **BREAKING**: Replaced manual Base64 encoding with HTTPBasicAuth
  - Old: 8+ lines of manual encoding
  - New: Single `HTTPBasicAuth` object
  
- 🔥 **BREAKING**: New unified client interface
  - Old: Direct API calls with manual auth injection
  - New: `client.assets.list()` pattern with sub-clients
  
- 🔥 **BREAKING**: Import path changes
  - Old: `from src.rapid7.api_r7_isvm import ...`
  - New: `from rapid7 import InsightVMClient`
  
- 🔥 **BREAKING**: Environment variable format
  - Old: `ivm_host`, `ivm_port` (separate variables)
  - New: `INSIGHTVM_BASE_URL` (combined URL with protocol)
  - Old: Custom names like `ivm_username`
  - New: Standardized `INSIGHTVM_API_USERNAME`

#### Improvements
- ⚡ Simplified authentication (1 line vs 8+ lines)
- ⚡ Consistent API patterns across all modules
- ⚡ Better error handling with specific exception types
- ⚡ Type safety with comprehensive type hints
- ⚡ Cleaner code structure with package organization
- ⚡ Enterprise SSL certificate support (self-signed)

### Removed

#### Deprecated Files
- ❌ `src/rapid7/api_r7_auth.py` → Replaced by `auth.py`
- ❌ `src/rapid7/api_r7_auth_class.py` → Replaced by `auth.py`
- ❌ `src/rapid7/api_r7_api.py` → Replaced by `api/base.py`
- ❌ `src/rapid7/api_r7_asset_group.py` → Replaced by `api/asset_groups.py`
- ❌ `src/rapid7/api_r7_assets.py` → Functionality in `api/assets.py`
- ❌ `src/rapid7/api_r7_isvm.py` → Functionality in `api/assets.py`
- ❌ `src/rapid7/api_r7_isvm_get_assets.py` → Functionality in `api/assets.py`
- ❌ `src/client.py` → Replaced by `src/rapid7/client.py`

### Fixed
- 🐛 SSL certificate verification now configurable for self-signed certificates
- 🐛 Timeout handling consistent across all HTTP methods
- 🐛 Import conflicts resolved with clean package structure
- 🐛 Credential validation prevents runtime errors

### Testing
- ✅ Verified against live InsightVM instance
- ✅ Successfully retrieved 1182+ assets
- ✅ Authentication with HTTPBasicAuth confirmed working
- ✅ Self-signed certificate handling tested
- ✅ Asset group creation and management validated

### Migration Notes

**For users upgrading from v1.0**, please review [MIGRATION.md](MIGRATION.md) for:
- Step-by-step migration instructions
- Code comparison examples
- Environment variable updates
- Import statement changes
- Common migration patterns

**Estimated migration time**: 30-60 minutes for typical usage

## [1.0.0] - Previous

### Initial Release Features

- Basic InsightVM API integration
- Functional authentication approach
- Asset retrieval capabilities
- Asset group creation
- Database storage support (PostgreSQL)
- Palo Alto Cortex XDR integration
- Agent installation tools
- Manual Base64 authentication

### Known Issues (Fixed in v2.0)
- Manual authentication implementation (8+ lines)
- Scattered authentication code across multiple files
- No SSL verification configuration
- Inconsistent timeout handling
- Import conflicts with circular dependencies

---

## Versioning Strategy

We use [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0) - Incompatible API changes
- **MINOR** version (0.X.0) - New functionality (backward compatible)
- **PATCH** version (0.0.X) - Bug fixes (backward compatible)

## Release Types

- **🎉 Major Release** - Breaking changes, new architecture
- **✨ Minor Release** - New features, backward compatible
- **🐛 Patch Release** - Bug fixes only

## Categories

Changes are categorized as:

- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security improvements

## Links

- [v2.0.0 Migration Guide](MIGRATION.md)
- [API Reference](docs/API_REFERENCE.md)
- [Usage Examples](docs/EXAMPLES.md)
- [Contributing](CONTRIBUTING.md)
- [GitHub Repository](https://github.com/talltechy/insightvm-python)

---

**Note**: Pre-v1.0 development history not included in this changelog.
