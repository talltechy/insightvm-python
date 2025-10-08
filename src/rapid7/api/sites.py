"""
Module for Site API operations.

This module provides a standard interface for managing sites through the
InsightVM API v3. It supports CRUD operations and site-related queries.
"""

from typing import Dict, Any, List, Optional, Tuple
from .base import BaseAPI


class SiteAPI(BaseAPI):
    """
    API client for Site operations.
    
    This class provides methods for managing sites including creating,
    updating, deleting sites, and querying site-related information.
    
    All methods return JSON responses from the API.
    
    Example:
        >>> from rapid7 import InsightVMClient
        >>> client = InsightVMClient()
        >>> 
        >>> # List all sites
        >>> sites = client.sites.list()
        >>> 
        >>> # Get specific site
        >>> site = client.sites.get(123)
        >>> 
        >>> # Create new site
        >>> new_site = client.sites.create(
        ...     name="Production Servers",
        ...     description="Critical infrastructure"
        ... )
    """
    
    def __init__(
        self,
        auth,
        verify_ssl: Optional[bool] = None,
        timeout: Tuple[int, int] = (10, 90)
    ):
        """
        Initialize the SiteAPI client.
        
        Args:
            auth: Authentication object (InsightVMAuth instance)
            verify_ssl: Whether to verify SSL certificates
            timeout: Tuple of (connect_timeout, read_timeout) in seconds
        """
        super().__init__(auth, verify_ssl, timeout)
    
    # ==================== Core CRUD Operations ====================
    
    def list(self, **params) -> Dict[str, Any]:
        """
        List all sites.
        
        Supports pagination and sorting through query parameters.
        
        Args:
            **params: Optional query parameters including:
                - page: Page number (0-indexed)
                - size: Number of results per page (max 500)
                - sort: Sort criteria (e.g., 'name', 'id')
        
        Returns:
            Dictionary containing:
                - resources: List of site objects
                - page: Pagination information
                - links: Hypermedia links
        
        Example:
            >>> sites = client.sites.list(page=0, size=100)
            >>> for site in sites['resources']:
            ...     print(f"{site['id']}: {site['name']}")
        """
        return self._request('GET', 'sites', params=params)
    
    def get_site(self, site_id: int) -> Dict[str, Any]:
        """
        Get details for a specific site.
        
        Args:
            site_id: The identifier of the site
        
        Returns:
            Dictionary containing comprehensive site configuration including:
                - id: Site identifier
                - name: Site name
                - description: Site description
                - type: Site type (static, dynamic, etc.)
                - importance: Site importance (low, normal, high)
                - scanEngine: Scan engine configuration
                - scanTemplate: Scan template configuration
                - assets: Asset count
                - links: Hypermedia links
        
        Example:
            >>> site = client.sites.get_site(123)
            >>> print(f"Site: {site['name']}")
            >>> print(f"Type: {site['type']}")
            >>> print(f"Assets: {site['assets']}")
        """
        return self._request('GET', f'sites/{site_id}')
    
    def create(
        self,
        name: str,
        description: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new site.
        
        Creates a site with specified configuration. Sites can be configured
        with various settings including scan engines, templates, importance,
        and target specifications.
        
        Args:
            name: Name for the site (required)
            description: Description of the site purpose
            **kwargs: Site configuration options including:
                - importance: Site importance (low, normal, high)
                - scanEngineId: ID of scan engine to use
                - scanTemplateId: ID of scan template to use
                - type: Site type (static, dynamic, agent)
                - includedTargets: Targets to include in scans
                - excludedTargets: Targets to exclude from scans
                - includedAssetGroups: Asset groups to include
                - excludedAssetGroups: Asset groups to exclude
        
        Returns:
            Dictionary containing:
                - id: New site identifier
                - links: Hypermedia links
        
        Example:
            >>> site = client.sites.create(
            ...     name="Production Network",
            ...     description="Production infrastructure scan",
            ...     importance="high",
            ...     scanEngineId=1,
            ...     scanTemplateId="full-audit-without-web-spider"
            ... )
            >>> print(f"Created site: {site['id']}")
        """
        data = {
            'name': name,
            'description': description,
            **kwargs
        }
        return self._request('POST', 'sites', json=data)
    
    def update(self, site_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update an existing site.
        
        Modifies the configuration of an existing site.
        
        Args:
            site_id: The identifier of the site
            **kwargs: Site properties to update (name, description,
                     importance, scanEngineId, scanTemplateId, etc.)
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.sites.update(
            ...     123,
            ...     name="Updated Production Network",
            ...     importance="high"
            ... )
        """
        return self._request('PUT', f'sites/{site_id}', json=kwargs)
    
    def delete_site(self, site_id: int) -> Dict[str, Any]:
        """
        Delete a site.
        
        Removes a site from the system. This operation cannot be undone.
        
        Args:
            site_id: The identifier of the site
        
        Returns:
            Dictionary containing deletion confirmation and links
        
        Example:
            >>> result = client.sites.delete_site(123)
        """
        return self._request('DELETE', f'sites/{site_id}')
    
    # ==================== Site Assets ====================
    
    def get_assets(self, site_id: int, **params) -> Dict[str, Any]:
        """
        Get assets for a specific site.
        
        Retrieves all assets that are part of the specified site.
        
        Args:
            site_id: The identifier of the site
            **params: Optional query parameters including:
                - page: Page number (0-indexed)
                - size: Number of results per page
                - sort: Sort criteria
        
        Returns:
            Dictionary containing:
                - resources: List of asset objects
                - page: Pagination information
                - links: Hypermedia links
        
        Example:
            >>> assets = client.sites.get_assets(123, page=0, size=100)
            >>> for asset in assets['resources']:
            ...     print(f"{asset['ip']}: {asset['hostName']}")
        """
        return self._request('GET', f'sites/{site_id}/assets', params=params)
    
    # ==================== Site Configuration ====================
    
    def get_scan_engine(self, site_id: int) -> Dict[str, Any]:
        """
        Get the scan engine assigned to a site.
        
        Retrieves details about the scan engine that will be used
        to scan the site.
        
        Args:
            site_id: The identifier of the site
        
        Returns:
            Dictionary containing scan engine configuration
        
        Example:
            >>> engine = client.sites.get_scan_engine(123)
            >>> print(f"Engine: {engine['name']}")
            >>> print(f"Status: {engine['status']}")
        """
        return self._request('GET', f'sites/{site_id}/scan_engine')
    
    def get_scan_template(self, site_id: int) -> Dict[str, Any]:
        """
        Get the scan template assigned to a site.
        
        Retrieves details about the scan template configuration
        that will be used when scanning the site.
        
        Args:
            site_id: The identifier of the site
        
        Returns:
            Dictionary containing scan template configuration
        
        Example:
            >>> template = client.sites.get_scan_template(123)
            >>> print(f"Template: {template['name']}")
            >>> print(f"Discovery only: {template['discoveryOnly']}")
        """
        return self._request('GET', f'sites/{site_id}/scan_template')
    
    def set_scan_engine(
        self,
        site_id: int,
        engine_id: int
    ) -> Dict[str, Any]:
        """
        Set the scan engine for a site.
        
        Assigns a specific scan engine to be used for scanning the site.
        
        Args:
            site_id: The identifier of the site
            engine_id: The identifier of the scan engine
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.sites.set_scan_engine(123, engine_id=5)
        """
        return self._request(
            'PUT',
            f'sites/{site_id}/scan_engine',
            json={'id': engine_id}
        )
    
    def set_scan_template(
        self,
        site_id: int,
        template_id: str
    ) -> Dict[str, Any]:
        """
        Set the scan template for a site.
        
        Assigns a specific scan template to be used for scanning the site.
        
        Args:
            site_id: The identifier of the site
            template_id: The identifier of the scan template
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.sites.set_scan_template(
            ...     123,
            ...     template_id="full-audit-without-web-spider"
            ... )
        """
        return self._request(
            'PUT',
            f'sites/{site_id}/scan_template',
            json={'id': template_id}
        )
    
    # ==================== Site Scans ====================
    
    def get_scans(self, site_id: int, **params) -> Dict[str, Any]:
        """
        Get scans for a specific site.
        
        Retrieves historical and active scans for the specified site.
        
        Args:
            site_id: The identifier of the site
            **params: Optional query parameters including:
                - page: Page number (0-indexed)
                - size: Number of results per page
                - sort: Sort criteria
                - active: Filter for active scans only
        
        Returns:
            Dictionary containing:
                - resources: List of scan objects
                - page: Pagination information
                - links: Hypermedia links
        
        Example:
            >>> scans = client.sites.get_scans(123)
            >>> for scan in scans['resources']:
            ...     print(f"Scan {scan['id']}: {scan['status']}")
        """
        return self._request('GET', f'sites/{site_id}/scans', params=params)
    
    def start_scan(
        self,
        site_id: int,
        hosts: Optional[List[str]] = None,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Start a scan for a site.
        
        Initiates a new scan for the specified site. Optionally can
        specify specific hosts to scan.
        
        Args:
            site_id: The identifier of the site
            hosts: Optional list of specific hosts to scan
            name: Optional name for the scan
        
        Returns:
            Dictionary containing:
                - id: Scan identifier
                - links: Hypermedia links including scan status
        
        Example:
            >>> # Scan entire site
            >>> scan = client.sites.start_scan(123)
            >>> print(f"Started scan: {scan['id']}")
            >>> 
            >>> # Scan specific hosts
            >>> scan = client.sites.start_scan(
            ...     123,
            ...     hosts=["192.168.1.100", "192.168.1.101"],
            ...     name="Targeted scan"
            ... )
        """
        data: Dict[str, Any] = {}
        if hosts:
            data['hosts'] = hosts
        if name:
            data['name'] = name
        
        return self._request('POST', f'sites/{site_id}/scans', json=data)
    
    # ==================== Site Targets ====================
    
    def get_included_targets(self, site_id: int) -> Dict[str, Any]:
        """
        Get the included targets for a site.
        
        Retrieves the list of targets that are included in site scans.
        
        Args:
            site_id: The identifier of the site
        
        Returns:
            Dictionary containing included target addresses
        
        Example:
            >>> targets = client.sites.get_included_targets(123)
            >>> print(f"Included: {targets['addresses']}")
        """
        return self._request('GET', f'sites/{site_id}/included_targets')
    
    def get_excluded_targets(self, site_id: int) -> Dict[str, Any]:
        """
        Get the excluded targets for a site.
        
        Retrieves the list of targets that are excluded from site scans.
        
        Args:
            site_id: The identifier of the site
        
        Returns:
            Dictionary containing excluded target addresses
        
        Example:
            >>> targets = client.sites.get_excluded_targets(123)
            >>> print(f"Excluded: {targets['addresses']}")
        """
        return self._request('GET', f'sites/{site_id}/excluded_targets')
    
    def set_included_targets(
        self,
        site_id: int,
        addresses: List[str]
    ) -> Dict[str, Any]:
        """
        Set the included targets for a site.
        
        Defines which targets should be included in site scans.
        Accepts IP addresses, ranges, and hostnames.
        
        Args:
            site_id: The identifier of the site
            addresses: List of target addresses (IPs, ranges, hostnames)
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.sites.set_included_targets(
            ...     123,
            ...     addresses=[
            ...         "192.168.1.0/24",
            ...         "10.0.0.1-10.0.0.50",
            ...         "server.example.com"
            ...     ]
            ... )
        """
        return self._request(
            'PUT',
            f'sites/{site_id}/included_targets',
            json={'addresses': addresses}
        )
    
    def set_excluded_targets(
        self,
        site_id: int,
        addresses: List[str]
    ) -> Dict[str, Any]:
        """
        Set the excluded targets for a site.
        
        Defines which targets should be excluded from site scans.
        Accepts IP addresses, ranges, and hostnames.
        
        Args:
            site_id: The identifier of the site
            addresses: List of target addresses to exclude
        
        Returns:
            Dictionary containing update confirmation and links
        
        Example:
            >>> result = client.sites.set_excluded_targets(
            ...     123,
            ...     addresses=["192.168.1.1", "192.168.1.254"]
            ... )
        """
        return self._request(
            'PUT',
            f'sites/{site_id}/excluded_targets',
            json={'addresses': addresses}
        )
