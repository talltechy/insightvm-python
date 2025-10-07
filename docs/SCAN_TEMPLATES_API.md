# Scan Templates API Documentation

## Overview

The Scan Templates API module provides comprehensive functionality for managing scan templates in Rapid7 InsightVM. Scan templates define the configuration for vulnerability scans, including which vulnerability checks to perform, discovery settings, performance parameters, and authentication options.

## Quick Start

```python
from rapid7 import InsightVMClient

# Initialize client
client = InsightVMClient()

# List all scan templates
templates = client.scan_templates.list()
for template in templates['resources']:
    print(f"{template['name']}: {template['id']}")

# Get specific template details
template = client.scan_templates.get(template_id='full-audit-without-web-spider')
print(f"Template: {template['name']}")
print(f"Checks: {template['checks']['categories']}")

# Create a custom template
template = client.scan_templates.create(
    name="Custom Production Template",
    description="Template for production asset scanning",
    checks={
        'categories': ['windows', 'unix', 'malware', 'policy']
    }
)
print(f"Created template: {template['id']}")
```

## Scan Template Operations

### List All Scan Templates

List all available scan templates (both built-in and custom):

```python
templates = client.scan_templates.list()

for template in templates['resources']:
    print(f"ID: {template['id']}")
    print(f"Name: {template['name']}")
    print(f"Description: {template.get('description', 'N/A')}")
    print(f"Built-in: {template.get('builtin', False)}")
    print("---")
```

### Get Scan Template Details

Retrieve detailed configuration for a specific scan template:

```python
template = client.scan_templates.get(
    template_id='discovery'
)

print(f"Template Name: {template['name']}")
print(f"Description: {template.get('description')}")
print(f"Vulnerability Checks: {template.get('checks', {})}")
print(f"Discovery Settings: {template.get('discovery', {})}")
print(f"Performance: {template.get('performance', {})}")
```

### Create Custom Scan Template

Create a new scan template with custom configuration:

```python
# Create basic template
template = client.scan_templates.create(
    name="Custom Production Template",
    description="Template for production asset scanning",
    checks={
        'categories': ['windows', 'unix', 'malware'],
        'individual': [],
        'unsafe': False
    }
)

# Create advanced template with full configuration
template = client.scan_templates.create(
    name="Advanced Custom Template",
    description="Comprehensive scanning with custom settings",
    checks={
        'categories': ['windows', 'unix', 'malware', 'policy'],
        'individual': ['ssh-weak-algorithms', 'ssl-weak-ciphers'],
        'unsafe': False,
        'correlate': True
    },
    discovery={
        'asset': {
            'ipAddressDiscovery': True,
            'collectWhoisInformation': True
        },
        'service': {
            'serviceNameDiscovery': True,
            'tcpPorts': {'type': 'well-known'},
            'udpPorts': {'type': 'well-known'}
        },
        'performance': {
            'scanDelay': 0,
            'packetRate': 'adaptive',
            'parallelAssets': 10,
            'parallelMinPorts': 0,
            'parallelMaxPorts': 0
        }
    },
    enableWindowsServices=True,
    enableSNMPCollection=True
)
```

### Update Scan Template

Modify an existing scan template:

```python
# Update template name and description
result = client.scan_templates.update(
    template_id='my-custom-template',
    name="Updated Template Name",
    description="Updated description"
)

# Update vulnerability checks
result = client.scan_templates.update(
    template_id='my-custom-template',
    checks={
        'categories': ['windows', 'unix', 'web'],
        'correlate': True
    }
)

# Enable unsafe checks (use with caution)
result = client.scan_templates.update(
    template_id='my-custom-template',
    checks={
        'unsafe': True
    }
)
```

### Delete Scan Template

Remove a custom scan template (built-in templates cannot be deleted):

```python
result = client.scan_templates.delete(template_id='my-custom-template')
```

## Discovery Configuration

### Get Discovery Settings

Retrieve discovery configuration from a template:

```python
discovery = client.scan_templates.get_discovery(
    template_id='full-audit'
)

print(f"Asset Discovery: {discovery.get('asset', {})}")
print(f"Service Discovery: {discovery.get('service', {})}")
print(f"Performance: {discovery.get('performance', {})}")
```

### Update Discovery Settings

Modify discovery configuration for a template:

```python
# Update asset discovery
result = client.scan_templates.update_discovery(
    template_id='my-template',
    asset={
        'ipAddressDiscovery': True,
        'collectWhoisInformation': True,
        'ipv6Discovery': True
    }
)

# Update service discovery
result = client.scan_templates.update_discovery(
    template_id='my-template',
    service={
        'serviceNameDiscovery': True,
        'tcpPorts': {'type': 'custom', 'ports': [22, 80, 443, 3389, 8080]},
        'udpPorts': {'type': 'well-known'}
    }
)

# Update performance settings
result = client.scan_templates.update_discovery(
    template_id='my-template',
    performance={
        'scanDelay': 5,
        'packetRate': 'adaptive',
        'parallelAssets': 20,
        'parallelMinPorts': 0,
        'parallelMaxPorts': 0
    }
)
```

## Service Discovery Operations

### Get Service Discovery Settings

Retrieve service discovery configuration:

```python
service_discovery = client.scan_templates.get_service_discovery(
    template_id='full-audit'
)

print(f"Service Name Discovery: {service_discovery.get('serviceNameDiscovery')}")
print(f"TCP Ports: {service_discovery.get('tcpPorts')}")
print(f"UDP Ports: {service_discovery.get('udpPorts')}")
```

### Update Service Discovery Settings

Modify service discovery configuration:

```python
# Well-known ports only
result = client.scan_templates.update_service_discovery(
    template_id='my-template',
    serviceNameDiscovery=True,
    tcpPorts={'type': 'well-known'},
    udpPorts={'type': 'well-known'}
)

# Custom port ranges
result = client.scan_templates.update_service_discovery(
    template_id='my-template',
    serviceNameDiscovery=True,
    tcpPorts={
        'type': 'custom',
        'ports': [22, 80, 443, 3389, 8080, 8443]
    },
    udpPorts={
        'type': 'range',
        'start': 1,
        'end': 1024
    }
)

# All TCP ports (thorough but slow)
result = client.scan_templates.update_service_discovery(
    template_id='my-template',
    tcpPorts={'type': 'all'}
)
```

## Helper Methods

### Get Built-in Templates

Filter templates to show only built-in ones:

```python
builtin_templates = client.scan_templates.get_builtin_templates()

for template in builtin_templates:
    print(f"{template['name']}: {template['id']}")
```

### Clone Template

Create a copy of an existing template:

```python
# Clone a built-in template
new_template = client.scan_templates.clone_template(
    template_id='full-audit',
    new_name="My Custom Full Audit",
    new_description="Customized full audit template"
)
print(f"Created clone: {new_template['id']}")
```

### Configure Performance

Set performance parameters for optimal scanning:

```python
# Conservative settings (slower, safer)
result = client.scan_templates.configure_performance(
    template_id='my-template',
    scan_delay=10,
    packet_rate='slow',
    parallel_assets=5
)

# Aggressive settings (faster, may impact network)
result = client.scan_templates.configure_performance(
    template_id='my-template',
    scan_delay=0,
    packet_rate='fast',
    parallel_assets=50
)

# Adaptive settings (balanced)
result = client.scan_templates.configure_performance(
    template_id='my-template',
    packet_rate='adaptive',
    parallel_assets=20
)
```

### Enable Vulnerability Categories

Enable specific vulnerability check categories:

```python
# Enable multiple categories
result = client.scan_templates.enable_vulnerability_categories(
    template_id='my-template',
    categories=['windows', 'unix', 'web', 'database', 'malware', 'policy']
)

# Enable all available categories
result = client.scan_templates.enable_vulnerability_categories(
    template_id='my-template',
    categories=[
        'aix', 'as400', 'bsd', 'cisco', 'cups', 'database',
        'db2', 'debian', 'docker', 'f5', 'fortinet', 'hp-ux',
        'huawei', 'ibm', 'industrial', 'informix', 'ios', 'juniper',
        'linux', 'mac-os', 'mainframe', 'malware', 'microsoft',
        'mobile', 'mysql', 'netware', 'office', 'oracle',
        'palo-alto', 'policy', 'postgresql', 'printer', 'redhat',
        'scada', 'smtp', 'snmp', 'solaris', 'sql-server',
        'ssh', 'ssl', 'suse', 'sybase', 'ubuntu', 'unix',
        'vmware', 'vpn', 'web', 'windows', 'wireless'
    ]
)
```

### Disable Vulnerability Categories

Disable specific vulnerability check categories:

```python
# Disable categories not needed for specific assets
result = client.scan_templates.disable_vulnerability_categories(
    template_id='my-template',
    categories=['mobile', 'wireless', 'scada', 'industrial']
)
```

### Create Discovery Template

Create a template optimized for asset discovery:

```python
# Quick discovery template
template = client.scan_templates.create_discovery_template(
    name="Quick Network Discovery",
    description="Fast network and service discovery",
    collect_whois=True,
    service_name_discovery=True,
    tcp_ports='well-known',
    udp_ports='well-known'
)

# Comprehensive discovery template
template = client.scan_templates.create_discovery_template(
    name="Comprehensive Discovery",
    description="Thorough asset and service discovery",
    collect_whois=True,
    ipv6_discovery=True,
    service_name_discovery=True,
    tcp_ports='all',
    udp_ports='custom',
    custom_udp_ports=[53, 123, 161, 162, 500]
)
```

## Common Use Cases

### Create Production Scanning Template

Create a template optimized for production environments:

```python
# Clone a built-in template
base_template = client.scan_templates.clone_template(
    template_id='full-audit-without-web-spider',
    new_name="Production Full Audit",
    new_description="Customized for production scanning"
)

template_id = base_template['id']

# Configure conservative performance
client.scan_templates.configure_performance(
    template_id=template_id,
    scan_delay=5,
    packet_rate='adaptive',
    parallel_assets=10
)

# Enable relevant checks only
client.scan_templates.enable_vulnerability_categories(
    template_id=template_id,
    categories=['windows', 'unix', 'linux', 'web', 'database', 'ssl']
)

# Disable intensive checks
client.scan_templates.disable_vulnerability_categories(
    template_id=template_id,
    categories=['mobile', 'wireless', 'scada', 'industrial']
)

print(f"Production template ready: {template_id}")
```

### Create Development/Test Template

Create an aggressive template for development environments:

```python
template = client.scan_templates.create(
    name="Development Full Scan",
    description="Comprehensive scanning for development",
    checks={
        'categories': ['windows', 'unix', 'web', 'database', 'malware'],
        'unsafe': True,  # Enable unsafe checks in dev
        'correlate': True
    }
)

# Configure aggressive performance
client.scan_templates.configure_performance(
    template_id=template['id'],
    scan_delay=0,
    packet_rate='fast',
    parallel_assets=50
)
```

### Create Compliance Scanning Template

Create a template for compliance auditing:

```python
# Start with policy template
template = client.scan_templates.clone_template(
    template_id='policy',
    new_name="Compliance Audit Template",
    new_description="PCI DSS, HIPAA, and CIS compliance"
)

template_id = template['id']

# Enable policy and configuration checks
client.scan_templates.enable_vulnerability_categories(
    template_id=template_id,
    categories=['policy', 'windows', 'unix', 'ssl', 'database']
)

# Add specific checks
client.scan_templates.update(
    template_id=template_id,
    checks={
        'individual': [
            'ssl-weak-ciphers',
            'ssl-certificate-expiry',
            'ssh-weak-algorithms',
            'smb-signing-disabled'
        ],
        'correlate': True
    }
)
```

### Review and Optimize Existing Templates

Audit existing templates and optimize:

```python
# Get all custom templates (exclude built-in)
all_templates = client.scan_templates.list()
custom_templates = [
    t for t in all_templates['resources']
    if not t.get('builtin', False)
]

print(f"Found {len(custom_templates)} custom templates")

for template in custom_templates:
    template_id = template['id']
    
    # Get full details
    details = client.scan_templates.get(template_id)
    
    print(f"\nTemplate: {details['name']}")
    print(f"Categories: {details.get('checks', {}).get('categories', [])}")
    
    # Get discovery settings
    discovery = client.scan_templates.get_discovery(template_id)
    performance = discovery.get('performance', {})
    
    print(f"Scan Delay: {performance.get('scanDelay', 0)}ms")
    print(f"Parallel Assets: {performance.get('parallelAssets', 0)}")
    print(f"Packet Rate: {performance.get('packetRate', 'unknown')}")
```

### Standardize Templates Across Organization

Create a consistent set of templates:

```python
# Define standard templates
standard_templates = {
    'production': {
        'name': 'Standard Production Scan',
        'categories': ['windows', 'unix', 'web', 'ssl'],
        'performance': {'scan_delay': 5, 'parallel_assets': 10}
    },
    'development': {
        'name': 'Standard Development Scan',
        'categories': ['windows', 'unix', 'web', 'database', 'malware'],
        'performance': {'scan_delay': 0, 'parallel_assets': 50}
    },
    'compliance': {
        'name': 'Standard Compliance Scan',
        'categories': ['policy', 'windows', 'unix', 'ssl'],
        'performance': {'scan_delay': 10, 'parallel_assets': 5}
    }
}

# Create each standard template
for key, config in standard_templates.items():
    # Create template
    template = client.scan_templates.create(
        name=config['name'],
        description=f"Standard {key} template",
        checks={'categories': config['categories']}
    )
    
    # Configure performance
    client.scan_templates.configure_performance(
        template_id=template['id'],
        scan_delay=config['performance']['scan_delay'],
        parallel_assets=config['performance']['parallel_assets']
    )
    
    print(f"Created: {config['name']}")
```

## Error Handling

Handle common error scenarios:

```python
from requests.exceptions import HTTPError

try:
    template = client.scan_templates.get(template_id='non-existent')
except HTTPError as e:
    if e.response.status_code == 404:
        print("Template not found")
    elif e.response.status_code == 401:
        print("Authentication failed")
    else:
        print(f"Error: {e}")

# Prevent accidental deletion of built-in templates
try:
    client.scan_templates.delete(template_id='discovery')
except HTTPError as e:
    if e.response.status_code == 400:
        print("Cannot delete built-in template")
```

## Response Examples

### Template Response

```json
{
  "id": "my-custom-template",
  "name": "Custom Production Template",
  "description": "Template for production asset scanning",
  "builtin": false,
  "checks": {
    "categories": ["windows", "unix", "malware", "policy"],
    "individual": ["ssl-weak-ciphers", "ssh-weak-algorithms"],
    "unsafe": false,
    "correlate": true
  },
  "discovery": {
    "asset": {
      "ipAddressDiscovery": true,
      "collectWhoisInformation": true,
      "ipv6Discovery": false
    },
    "service": {
      "serviceNameDiscovery": true,
      "tcpPorts": {"type": "well-known"},
      "udpPorts": {"type": "well-known"}
    },
    "performance": {
      "scanDelay": 5,
      "packetRate": "adaptive",
      "parallelAssets": 10,
      "parallelMinPorts": 0,
      "parallelMaxPorts": 0
    }
  },
  "enableWindowsServices": true,
  "enableSNMPCollection": true,
  "links": [
    {
      "href": "https://hostname:3780/api/3/scan_templates/my-custom-template",
      "rel": "self"
    }
  ]
}
```

### Discovery Settings Response

```json
{
  "asset": {
    "ipAddressDiscovery": true,
    "collectWhoisInformation": true,
    "ipv6Discovery": true,
    "fingerprintMinimumCertainty": "0.16"
  },
  "service": {
    "serviceNameDiscovery": true,
    "tcpPorts": {
      "type": "custom",
      "ports": [22, 80, 443, 3389, 8080, 8443]
    },
    "udpPorts": {
      "type": "well-known"
    }
  },
  "performance": {
    "scanDelay": 0,
    "packetRate": "adaptive",
    "parallelAssets": 20,
    "parallelMinPorts": 0,
    "parallelMaxPorts": 0
  }
}
```

## API Methods Reference

### Core Template Operations
- `list(**params)` - List all scan templates
- `get(template_id)` - Get template details
- `create(name, description, **kwargs)` - Create template
- `update(template_id, **kwargs)` - Update template
- `delete(template_id)` - Delete template

### Discovery Operations
- `get_discovery(template_id)` - Get discovery settings
- `update_discovery(template_id, **settings)` - Update discovery
- `get_service_discovery(template_id)` - Get service discovery
- `update_service_discovery(template_id, **settings)` - Update service discovery

### Helper Methods
- `get_builtin_templates()` - Get built-in templates
- `clone_template(template_id, new_name, new_description)` - Clone template
- `configure_performance(template_id, **settings)` - Set performance
- `enable_vulnerability_categories(template_id, categories)` - Enable checks
- `disable_vulnerability_categories(template_id, categories)` - Disable checks
- `create_discovery_template(name, description, **kwargs)` - Create discovery template

## Best Practices

1. **Start with Built-in Templates**: Clone and customize rather than creating from scratch
2. **Test in Development**: Validate new templates in dev before production use
3. **Document Customizations**: Clearly describe why custom templates exist
4. **Regular Reviews**: Periodically review and optimize template configurations
5. **Performance Tuning**: Adjust based on network capacity and scanning windows
6. **Unsafe Checks**: Only enable in controlled environments
7. **Standardization**: Create consistent templates across your organization
8. **Compliance Alignment**: Map templates to compliance requirements

## Available Vulnerability Categories

Common vulnerability check categories include:

- **Operating Systems**: windows, unix, linux, redhat, ubuntu, debian, suse, solaris, aix, bsd, hp-ux, mac-os
- **Network Devices**: cisco, juniper, f5, fortinet, palo-alto, huawei
- **Databases**: database, mysql, postgresql, oracle, sql-server, db2, sybase, informix
- **Applications**: web, office, cups, smtp, snmp, ssh, ssl, vpn
- **Specialized**: malware, policy, scada, industrial, mobile, wireless, docker, vmware, printer

## TCP/UDP Port Scan Options

Port scanning can be configured with these options:

- **well-known**: Ports 1-1024 (fast, covers common services)
- **all**: All ports 1-65535 (thorough but slow)
- **custom**: Specific list of ports
- **range**: Port range (start to end)
- **none**: No port scanning

## Performance Settings

### Scan Delay
- `0`: No delay (fastest, may impact network)
- `5`: Small delay (balanced)
- `10+`: Conservative (slower, network-friendly)

### Packet Rate
- `slow`: ~1 packet/sec (very conservative)
- `adaptive`: Adjusts based on network response (recommended)
- `fast`: Maximum speed (use with caution)

### Parallel Assets
- `1-5`: Conservative (slower scans)
- `10-20`: Balanced (recommended)
- `50+`: Aggressive (requires adequate resources)

## See Also

- [Scans API Documentation](SCANS_API.md) - Running scans with templates
- [Sites API Documentation](SITE_MANAGEMENT.md) - Assigning templates to sites
- [Scan Engines API Documentation](SCAN_ENGINES_API.md) - Managing scan engines
- [API Reference](API_REFERENCE.md) - Complete API documentation
