# Security Policy

## Supported Versions

The following versions of InsightVM-Python are currently supported with security updates:

| Version | Supported          | Notes                                    |
| ------- | ------------------ | ---------------------------------------- |
| 2.0.x   | :white_check_mark: | Current version with active support      |
| < 2.0   | :x:                | Legacy version - please upgrade to 2.0.x |

**Recommendation**: Always use the latest v2.0.x release for the most up-to-date security fixes and features.

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow these steps:

### Reporting Process

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Report security issues via one of these methods:
   - **Preferred**: Use [GitHub Security Advisories](https://github.com/talltechy/insightvm-python/security/advisories/new)
   - **Alternative**: Email the maintainers directly (check repository for contact info)

### What to Include

When reporting a vulnerability, please provide:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Any suggested fixes (if available)
- Your contact information for follow-up questions

### Response Timeline

- **Initial Response**: Within 48 hours of report
- **Status Updates**: Every 5 business days until resolved
- **Resolution Target**: Critical vulnerabilities within 7 days, others within 30 days

### Disclosure Policy

- We will work with you to understand and resolve the issue
- We will publicly acknowledge your responsible disclosure (unless you prefer to remain anonymous)
- Security advisories will be published after a fix is available
- We follow coordinated disclosure practices

## Security Considerations

### Authentication & Credentials

#### ✅ Best Practices

**Environment Variables (Development)**
```bash
# Use .env file for local development
INSIGHTVM_API_USERNAME=your_username
INSIGHTVM_API_PASSWORD=your_password
INSIGHTVM_BASE_URL=https://console:3780
```

**Secret Management (Production)**
- Use enterprise secret management services:
  - AWS Secrets Manager
  - Azure Key Vault
  - HashiCorp Vault
  - Kubernetes Secrets
- Rotate credentials regularly
- Use least-privilege access principles

#### ❌ Security Anti-Patterns

**Never do this:**
```python
# DON'T hardcode credentials
client = InsightVMClient(
    username="admin",  # NEVER hardcode
    password="password123",  # NEVER hardcode
    base_url="https://console:3780"
)
```

**Do this instead:**
```python
# Load from environment (secure)
from rapid7 import InsightVMClient
client = InsightVMClient()  # Loads from environment variables
```

### SSL/TLS Certificate Verification

#### Self-Signed Certificates

⚠️ **Important**: The library supports disabling SSL verification for self-signed certificates, but this should be used carefully.

**When to use `verify_ssl=False`:**
- Internal/trusted networks with self-signed certificates
- Development environments
- Testing against non-production instances

**Security implications:**
```python
# Disables certificate validation - use with caution
client = InsightVMClient(verify_ssl=False)
```

**This makes you vulnerable to:**
- Man-in-the-middle (MITM) attacks
- Certificate spoofing
- Intercepted credentials

**Recommended approach for production:**
1. Use proper CA-signed certificates
2. Keep `verify_ssl=True` (default)
3. If using self-signed certificates, add them to your system's trust store:
   ```python
   import certifi
   # Point to your custom CA bundle
   client = InsightVMClient(verify_ssl='/path/to/custom-ca-bundle.crt')
   ```

### API Authentication

**HTTPBasicAuth Security:**
- The library uses `requests.auth.HTTPBasicAuth` for API authentication
- Credentials are transmitted over HTTPS (encrypted)
- Basic auth is appropriate for server-to-server communication
- Always use HTTPS endpoints (never HTTP)

**Network Security:**
```python
# Ensure HTTPS is used
assert client.auth.base_url.startswith('https://'), "Must use HTTPS"
```

### Timeout Configuration

**Prevent resource exhaustion:**
```python
# Configure appropriate timeouts
client = InsightVMClient(
    timeout=(10, 90)  # (connect timeout, read timeout) in seconds
)
```

**Recommendations:**
- Connect timeout: 5-10 seconds
- Read timeout: 30-120 seconds depending on operation
- For long-running operations (scans, reports), use explicit timeouts:
  ```python
  client.scans.wait_for_completion(scan_id, timeout=3600)
  client.reports.generate_and_download(report_id, timeout=7200)
  ```

### Input Validation

**The library provides:**
- Type hints for all parameters
- Validation of pagination parameters (MAX_PAGE_SIZE constants)
- Timeout validation to prevent invalid values

**User responsibility:**
- Validate data before sending to API
- Sanitize file paths for downloads
- Validate IDs and numeric parameters

### Rate Limiting & Resource Protection

**Best practices:**
```python
import time

# Avoid overwhelming the API
for asset_id in asset_ids:
    asset = client.assets.get_asset(asset_id)
    time.sleep(0.1)  # Small delay between requests

# Use batch operations when available
all_assets = client.assets.get_all(batch_size=500)  # Efficient pagination
```

### Secure Data Handling

**Downloaded Reports:**
```python
# Reports often contain sensitive vulnerability data
content = client.reports.download(report_id, instance_id)

# Store securely with appropriate permissions
import os
output_path = "/secure/location/report.pdf.gz"
os.makedirs(os.path.dirname(output_path), mode=0o700, exist_ok=True)
with open(output_path, "wb") as f:
    os.chmod(output_path, 0o600)  # Owner read/write only
    f.write(content)
```

**Asset Data:**
- Asset data may contain PII (hostnames, IPs, user information)
- Follow your organization's data handling policies
- Consider data retention requirements
- Implement appropriate access controls

### Dependency Security

**Keep dependencies updated:**
```bash
# Check for known vulnerabilities
pip install safety
safety check -r requirements.txt

# Update dependencies regularly
pip install --upgrade -r requirements.txt
```

**Current dependencies:**
- `requests >= 2.31.0` - HTTP library with security fixes
- `urllib3 >= 2.0.0` - Updated for security improvements
- `python-dotenv >= 1.0.0` - Secure environment variable loading

### Logging & Monitoring

**Avoid logging sensitive data:**
```python
import logging

# DON'T log credentials
# logging.debug(f"Connecting with {username}:{password}")  # NEVER!

# DO log non-sensitive information
logging.info(f"Connected to {client.auth.base_url}")
logging.info(f"Retrieved {len(assets['resources'])} assets")
```

**Monitor for:**
- Failed authentication attempts
- Unusual API usage patterns
- Large data exports
- SSL verification bypasses in production

## Known Security Features

### ✅ Implemented Security Controls

1. **HTTPBasicAuth** - Industry-standard authentication
2. **Environment Variable Configuration** - No hardcoded credentials
3. **Configurable SSL Verification** - Can require certificate validation
4. **Timeout Protection** - Prevents hanging connections
5. **Type Hints** - Reduces type-related vulnerabilities
6. **Pagination Limits** - MAX_PAGE_SIZE prevents excessive data requests
7. **Context Manager Support** - Proper resource cleanup

### 🔄 Ongoing Security Improvements

- Automated dependency scanning
- Regular security audits
- Community vulnerability reports
- Security-focused code reviews

## Compliance Considerations

When using this library in regulated environments:

1. **Data Residency**: Ensure API endpoints comply with data residency requirements
2. **Audit Logging**: Implement comprehensive logging for compliance
3. **Access Controls**: Use role-based access control (RBAC) for API credentials
4. **Data Encryption**: Verify data is encrypted in transit (HTTPS) and at rest
5. **Retention Policies**: Implement data retention and deletion policies

## Security Checklist for Production Use

- [ ] Credentials stored in secure secret management system
- [ ] SSL certificate validation enabled (`verify_ssl=True`)
- [ ] Appropriate timeouts configured
- [ ] Error handling doesn't leak sensitive information
- [ ] Logging doesn't include credentials or PII
- [ ] Dependencies are up-to-date
- [ ] Network access properly restricted (firewall rules)
- [ ] Monitoring and alerting configured
- [ ] Incident response plan in place
- [ ] Regular security reviews scheduled

## Pre-commit & Secret Scanning

This repository supports pre-commit hooks and CI secret scanning to help prevent accidental credential leaks.

Local setup (recommended):

1. Install pre-commit:

```bash
pip install pre-commit
pre-commit install
```

2. Run pre-commit against all files to validate formatting and static checks:

```bash
pre-commit run --all-files
```

3. (Optional) Initialize detect-secrets baseline for your environment and review findings before committing:

```bash
detect-secrets scan --all-files > .secrets.baseline
# Review the baseline and remove false positives, do not include real secrets
```

CI scanning:

- This project includes `.github/workflows/secret-scan.yml` which runs `detect-secrets` (and optionally gitleaks) and uploads findings as artifacts for maintainers to review. The initial workflow is configured to be non-blocking so that maintainers can review existing findings and create a sanitized `.secrets.baseline`.
- After the baseline is established and reviewed, maintainers can update the workflow to fail on new detections.

Best practices:
- Never commit `.env` files with real credentials.
- If a secret is discovered in the repo, rotate the secret immediately and remove the secret from the repository history.
- Use a secret manager for production systems and CI.

## Additional Resources

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Rapid7 InsightVM Security](https://docs.rapid7.com/insightvm/security/)
- [Python Requests Security](https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification)

---

**Last Updated**: October 2025  
**Version**: 2.0.0

For general questions, see [README.md](README.md) or open a [GitHub issue](https://github.com/talltechy/insightvm-python/issues).
