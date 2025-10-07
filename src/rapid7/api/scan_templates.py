"""
Module for Scan Templates API operations.

This module provides a comprehensive interface for managing scan templates
through the InsightVM API v3. It supports full CRUD operations, discovery
configuration, performance tuning, and vulnerability check management.
"""

from typing import Dict, Any, List, Optional, Tuple
from .base import BaseAPI


class ScanTemplateAPI(BaseAPI):
    """
    API client for Scan Template operations.
    
    This class provides methods for managing scan templates, including
    creating, updating, deleting templates, configuring discovery settings,
    managing vulnerability checks, and tuning performance parameters.
    
    All methods return JSON responses from the API.
    
    Example:
        >>> from rapid7 import InsightVMClient
        >>> client = InsightVMClient()
        >>> 
        >>> # List all scan templates
        >>> templates = client.scan_templates.list()
        >>> 
        >>> # Get specific template
        >>> template = client.scan_templates.get('full-audit-without-web-spider')
        >>> 
        >>> # Create custom template
        >>> new_template = client.scan_templates.create(
        ...     name="Custom Security Scan",
        ...     description="Tailored scan for production environment"
        ... )
    """
    
    def __init__(
        self,
        auth,
        verify_ssl: Optional[bool] = None,
        timeout: Tuple[int, int] = (10, 90)
    ):
        """
        Initialize the ScanTemplateAPI client.
        
        Args:
            auth: Authentication object (InsightVMAuth instance)
            verify_ssl: Whether to verify SSL certificates
            timeout: Tuple of (connect_timeout, read_timeout) in seconds
        """
        super().__init__(auth, verify_ssl, timeout)
    
    # ==================== Core CRUD Operations ====================
    
    def list(self, **params) -> Dict[str, Any]:
        """
        List all available scan templates.
        
        Returns both built-in and custom scan templates with their
        configurations and settings.
        
        Args:
            **params: Optional query parameters (currently none supported by API)
        
        Returns:
            Dictionary containing:
                - resources: List of scan template objects
                - links: Hypermedia links
        
        Example:
            >>> templates = client.scan_templates.list()
            >>> for template in templates['resources']:
            ...     print(f"{template['name']}: {template['description']}")
        """
        return self._request('GET', 'scan_templates', params=params)
    
    def get(self, template_id: str) -> Dict[str, Any]:
        """
        Get details for a specific scan template.
        
        Args:
            template_id: The identifier of the scan template
        
        Returns:
            Dictionary containing comprehensive template configuration including:
                - id: Template identifier
                - name: Template name
                - description: Template description
                - checks: Vulnerability check configuration
                - discovery: Discovery settings (asset, performance, service)
                - database: Database configuration
                - policy: Policy settings
                - web: Web spider configuration
                - telnet: Telnet settings
                - links: Hypermedia links
        
        Example:
            >>> template = client.scan_templates.get('full-audit-without-web-spider')
            >>> print(f"Template: {template['name']}")
            >>> print(f"Discovery only: {template['discoveryOnly']}")
        """
        return self._request('GET', f'scan_templates/{template_id}')
    
    def create(self, name: str, description: str = "", **kwargs) -> Dict[str, Any]:
        """
        Create a new scan template.
        
        Creates a custom scan template with specified configuration. Templates
        can be configured with various settings including vulnerability checks,
        discovery parameters, performance tuning, and policy enforcement.
        
        Args:
            name: Name for the scan template
            description: Description of the template purpose
            **kwargs: Template configuration options including:
                - discoveryOnly: Whether this is discovery-only scan
                - checks: Vulnerability check configuration
                - discovery: Discovery settings
                - database: Database configuration
                - policy: Policy settings
                - web: Web spider configuration
                - maxParallelAssets: Maximum parallel assets
                - maxScanProcesses: Maximum scan processes
                - vulnerabilityEnabled: Enable vulnerability scanning
                - webEnabled: Enable web spider
                - policyEnabled: Enable policy scanning
        
        Returns:
            Dictionary containing:
                - id: New template identifier
                - links: Hypermedia links
        
        Example:
            >>> template = client.scan_templates.create(
            ...     name="Fast Discovery",
            ...     description="Quick network discovery scan",
            ...     discoveryOnly=True,
            ...     maxParallelAssets=50
            ... )
            >>> print(f"Created template: {template['id']}")
        """
        data = {
            'name': name,
            'description': description,
            **kwargs
        }
        return self._request('POST', 'scan_templates', json=data)
    
    def update(self, template_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update an existing scan template.
        
        Modifies the configuration of a custom scan template. Built-in
        templates cannot be modified directly but can be cloned.
        
        Args:
            template_id: The identifier of the scan template
            **kwargs: Template properties to update (name, description,
                     checks, discovery, policy, web, etc.)
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.scan_templates.update(
            ...     'custom-template-id',
            ...     name="Updated Template Name",
            ...     maxParallelAssets=100
            ... )
        """
        return self._request('PUT', f'scan_templates/{template_id}', json=kwargs)
    
    def delete(self, template_id: str) -> Dict[str, Any]:
        """
        Delete a scan template.
        
        Removes a custom scan template from the system. Built-in templates
        cannot be deleted.
        
        Args:
            template_id: The identifier of the scan template
        
        Returns:
            Dictionary containing deletion confirmation and links
        
        Example:
            >>> result = client.scan_templates.delete('custom-template-id')
        """
        return self._request('DELETE', f'scan_templates/{template_id}')
    
    # ==================== Discovery Configuration ====================
    
    def get_discovery(self, template_id: str) -> Dict[str, Any]:
        """
        Get discovery settings for a scan template.
        
        Retrieves the complete discovery configuration including asset
        discovery, service discovery, and performance settings.
        
        Args:
            template_id: The identifier of the scan template
        
        Returns:
            Dictionary containing discovery configuration:
                - asset: Asset discovery settings (ICMP, ARP, fingerprinting)
                - performance: Performance tuning (packet rate, parallelism)
                - service: Service discovery (TCP/UDP port scanning)
        
        Example:
            >>> discovery = client.scan_templates.get_discovery('full-audit')
            >>> print(f"TCP ports: {discovery['service']['tcp']['ports']}")
            >>> print(f"Max packet rate: {discovery['performance']['packetRate']['maximum']}")
        """
        return self._request('GET', f'scan_templates/{template_id}/discovery')
    
    def update_discovery(self, template_id: str, **settings) -> Dict[str, Any]:
        """
        Update discovery settings for a scan template.
        
        Modifies the discovery configuration including asset detection methods,
        service discovery parameters, and performance tuning.
        
        Args:
            template_id: The identifier of the scan template
            **settings: Discovery configuration options including:
                - asset: Asset discovery settings
                - performance: Performance parameters
                - service: Service discovery configuration
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.scan_templates.update_discovery(
            ...     'custom-template',
            ...     asset={
            ...         'sendIcmpPings': True,
            ...         'sendArpPings': True,
            ...         'tcpPorts': [22, 80, 443, 3389, 8080]
            ...     },
            ...     performance={
            ...         'packetRate': {'maximum': 10000, 'minimum': 500}
            ...     }
            ... )
        """
        return self._request('PUT', f'scan_templates/{template_id}/discovery', 
                           json=settings)
    
    def get_service_discovery(self, template_id: str) -> Dict[str, Any]:
        """
        Get service discovery settings for a scan template.
        
        Retrieves TCP and UDP port scanning configuration including scan
        methods, port ranges, and exclusions.
        
        Args:
            template_id: The identifier of the scan template
        
        Returns:
            Dictionary containing service discovery settings:
                - tcp: TCP port scanning configuration
                - udp: UDP port scanning configuration
                - serviceNameFile: Custom service name file
        
        Example:
            >>> service = client.scan_templates.get_service_discovery('full-audit')
            >>> print(f"TCP method: {service['tcp']['method']}")
            >>> print(f"UDP ports: {service['udp']['ports']}")
        """
        return self._request('GET', f'scan_templates/{template_id}/service_discovery')
    
    def update_service_discovery(self, template_id: str, **settings) -> Dict[str, Any]:
        """
        Update service discovery settings for a scan template.
        
        Modifies TCP/UDP port scanning configuration including scan methods,
        port ranges, and exclusions.
        
        Args:
            template_id: The identifier of the scan template
            **settings: Service discovery options including:
                - tcp: TCP scanning configuration
                - udp: UDP scanning configuration
                - serviceNameFile: Custom service definitions
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.scan_templates.update_service_discovery(
            ...     'custom-template',
            ...     tcp={
            ...         'method': 'SYN',
            ...         'ports': 'well-known',
            ...         'additionalPorts': [8080, 8443, 9000]
            ...     },
            ...     udp={
            ...         'ports': 'well-known'
            ...     }
            ... )
        """
        return self._request('PUT', f'scan_templates/{template_id}/service_discovery',
                           json=settings)
    
    # ==================== Helper Methods ====================
    
    def get_builtin_templates(self) -> List[Dict[str, Any]]:
        """
        Get list of all built-in scan templates.
        
        Returns standard InsightVM scan templates that come pre-configured.
        These cannot be modified but can be cloned to create custom versions.
        
        Returns:
            List of built-in template objects
        
        Example:
            >>> builtins = client.scan_templates.get_builtin_templates()
            >>> for template in builtins:
            ...     print(f"{template['id']}: {template['name']}")
        """
        response = self.list()
        templates = response.get('resources', [])
        # Built-in templates typically have specific IDs like 'full-audit-without-web-spider'
        # Custom templates have numeric IDs
        return [t for t in templates if not str(t.get('id', '')).isdigit()]
    
    def clone_template(self, template_id: str, new_name: str, 
                      new_description: str = "") -> Dict[str, Any]:
        """
        Clone an existing scan template.
        
        Creates a copy of an existing template (built-in or custom) with a
        new name. Useful for creating custom templates based on built-in ones.
        
        Args:
            template_id: The identifier of the template to clone
            new_name: Name for the new template
            new_description: Description for the new template
        
        Returns:
            Dictionary containing:
                - id: New template identifier
                - links: Hypermedia links
        
        Example:
            >>> # Clone built-in template
            >>> new_template = client.scan_templates.clone_template(
            ...     'full-audit-without-web-spider',
            ...     'Custom Full Audit',
            ...     'Modified full audit for production'
            ... )
            >>> print(f"Cloned template: {new_template['id']}")
        """
        # Get the source template
        source = self.get(template_id)
        
        # Remove fields that shouldn't be copied
        source.pop('id', None)
        source.pop('links', None)
        
        # Set new name and description
        source['name'] = new_name
        if new_description:
            source['description'] = new_description
        
        # Create the new template
        return self.create(**source)
    
    def configure_performance(self, template_id: str, 
                            max_parallel_assets: Optional[int] = None,
                            max_scan_processes: Optional[int] = None,
                            packet_rate_max: Optional[int] = None,
                            packet_rate_min: Optional[int] = None) -> Dict[str, Any]:
        """
        Configure performance settings for a scan template.
        
        Helper method to quickly adjust performance parameters without
        modifying the complete discovery configuration.
        
        Args:
            template_id: The identifier of the scan template
            max_parallel_assets: Maximum assets to scan in parallel
            max_scan_processes: Maximum scan processes
            packet_rate_max: Maximum packet rate
            packet_rate_min: Minimum packet rate
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.scan_templates.configure_performance(
            ...     'custom-template',
            ...     max_parallel_assets=100,
            ...     max_scan_processes=5,
            ...     packet_rate_max=15000
            ... )
        """
        update_data = {}
        
        if max_parallel_assets is not None:
            update_data['maxParallelAssets'] = max_parallel_assets
        if max_scan_processes is not None:
            update_data['maxScanProcesses'] = max_scan_processes
        
        # Update template-level settings
        if update_data:
            self.update(template_id, **update_data)
        
        # Update discovery performance if packet rates specified
        if packet_rate_max is not None or packet_rate_min is not None:
            discovery = self.get_discovery(template_id)
            perf = discovery.get('performance', {})
            packet_rate = perf.get('packetRate', {})
            
            if packet_rate_max is not None:
                packet_rate['maximum'] = packet_rate_max
            if packet_rate_min is not None:
                packet_rate['minimum'] = packet_rate_min
            
            perf['packetRate'] = packet_rate
            discovery['performance'] = perf
            
            return self.update_discovery(template_id, **discovery)
        
        return {'message': 'Performance settings updated'}
    
    def enable_vulnerability_categories(self, template_id: str, 
                                       categories: List[str]) -> Dict[str, Any]:
        """
        Enable specific vulnerability check categories.
        
        Activates vulnerability checks for specified categories without
        affecting other check configurations.
        
        Args:
            template_id: The identifier of the scan template
            categories: List of category identifiers to enable
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.scan_templates.enable_vulnerability_categories(
            ...     'custom-template',
            ...     ['Apache', 'Windows', 'SSL/TLS']
            ... )
        """
        template = self.get(template_id)
        checks = template.get('checks', {})
        check_categories = checks.get('categories', {})
        
        enabled = check_categories.get('enabled', [])
        disabled = check_categories.get('disabled', [])
        
        # Add to enabled, remove from disabled
        for category in categories:
            if category not in enabled:
                enabled.append(category)
            if category in disabled:
                disabled.remove(category)
        
        check_categories['enabled'] = enabled
        check_categories['disabled'] = disabled
        checks['categories'] = check_categories
        
        return self.update(template_id, checks=checks)
    
    def disable_vulnerability_categories(self, template_id: str,
                                        categories: List[str]) -> Dict[str, Any]:
        """
        Disable specific vulnerability check categories.
        
        Deactivates vulnerability checks for specified categories without
        affecting other check configurations.
        
        Args:
            template_id: The identifier of the scan template
            categories: List of category identifiers to disable
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.scan_templates.disable_vulnerability_categories(
            ...     'custom-template',
            ...     ['potentially-unsafe']
            ... )
        """
        template = self.get(template_id)
        checks = template.get('checks', {})
        check_categories = checks.get('categories', {})
        
        enabled = check_categories.get('enabled', [])
        disabled = check_categories.get('disabled', [])
        
        # Add to disabled, remove from enabled
        for category in categories:
            if category not in disabled:
                disabled.append(category)
            if category in enabled:
                enabled.remove(category)
        
        check_categories['enabled'] = enabled
        check_categories['disabled'] = disabled
        checks['categories'] = check_categories
        
        return self.update(template_id, checks=checks)
    
    def create_discovery_template(self, name: str, 
                                 description: str = "Network discovery only",
                                 tcp_ports: Optional[List[int]] = None,
                                 udp_ports: Optional[List[int]] = None,
                                 send_icmp: bool = True,
                                 send_arp: bool = True) -> Dict[str, Any]:
        """
        Create a discovery-only scan template.
        
        Helper method to quickly create a template configured for network
        discovery without vulnerability scanning.
        
        Args:
            name: Name for the template
            description: Template description
            tcp_ports: List of TCP ports to scan (default: well-known)
            udp_ports: List of UDP ports to scan (default: well-known)
            send_icmp: Whether to send ICMP pings
            send_arp: Whether to send ARP requests
        
        Returns:
            Dictionary containing:
                - id: New template identifier
                - links: Hypermedia links
        
        Example:
            >>> template = client.scan_templates.create_discovery_template(
            ...     name="Fast Discovery",
            ...     tcp_ports=[22, 80, 443, 3389],
            ...     send_icmp=True
            ... )
        """
        discovery_config = {
            'asset': {
                'sendIcmpPings': send_icmp,
                'sendArpPings': send_arp,
                'ipFingerprintingEnabled': True,
                'treatTcpResetAsAsset': True
            },
            'service': {
                'tcp': {
                    'method': 'SYN',
                    'ports': 'well-known'
                },
                'udp': {
                    'ports': 'well-known'
                }
            }
        }
        
        if tcp_ports:
            discovery_config['service']['tcp']['additionalPorts'] = tcp_ports
        if udp_ports:
            discovery_config['service']['udp']['additionalPorts'] = udp_ports
        
        return self.create(
            name=name,
            description=description,
            discoveryOnly=True,
            vulnerabilityEnabled=False,
            webEnabled=False,
            policyEnabled=False,
            discovery=discovery_config
        )
