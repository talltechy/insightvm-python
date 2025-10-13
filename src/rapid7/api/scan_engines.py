"""
Module for Scan Engines API operations.

This module provides a comprehensive interface for managing scan engines and
engine pools through the InsightVM API v3. It supports full CRUD operations,
health monitoring, site assignments, and pool management.
"""

from typing import Dict, Any, List, Optional, Tuple
from .base import BaseAPI


class ScanEngineAPI(BaseAPI):
    """
    API client for Scan Engine operations.

    This class provides methods for managing scan engines and engine pools,
    including creating, updating, deleting engines, managing engine pools,
    and monitoring engine health and assignments.

    All methods return JSON responses from the API.

    Example:
        >>> from rapid7 import InsightVMClient
        >>> client = InsightVMClient()
        >>>
        >>> # List all scan engines
        >>> engines = client.scan_engines.list()
        >>>
        >>> # Get specific engine details
        >>> engine = client.scan_engines.get_engine(engine_id=6)
        >>>
        >>> # Create engine pool
        >>> pool = client.scan_engines.create_pool(
        ...     name="Production Pool",
        ...     engine_ids=[1, 2, 3]
        ... )
    """

    def __init__(
        self,
        auth,
        verify_ssl: Optional[bool] = None,
        timeout: Tuple[int, int] = (10, 90)
    ):
        """
        Initialize the ScanEngineAPI client.

        Args:
            auth: Authentication object (InsightVMAuth instance)
            verify_ssl: Whether to verify SSL certificates
            timeout: Tuple of (connect_timeout, read_timeout) in seconds
        """
        super().__init__(auth, verify_ssl, timeout)

    # ==================== Scan Engine Operations ====================

    def list(self, **params) -> Dict[str, Any]:
        """
        List all scan engines available for scanning.

        Returns scan engines with details including address, status, version,
        assigned sites, and whether it's an AWS pre-authorized engine.

        Args:
            **params: Optional query parameters (currently none supported by API)

        Returns:
            Dictionary containing:
                - resources: List of scan engine objects
                - links: Hypermedia links

        Example:
            >>> engines = client.scan_engines.list()
            >>> for engine in engines['resources']:
            ...     print(f"{engine['name']}: {engine['status']}")
        """
        return self._request('GET', 'scan_engines', params=params)

    def get_engine(self, engine_id: int) -> Dict[str, Any]:
        """
        Get details for a specific scan engine.

        Args:
            engine_id: The identifier of the scan engine

        Returns:
            Dictionary containing scan engine details including:
                - id: Engine identifier
                - name: Engine name
                - address: Engine hostname/IP
                - port: Engine port number
                - status: Current status
                - productVersion: Engine software version
                - contentVersion: Content/vulnerability definitions version
                - sites: List of assigned site IDs
                - links: Hypermedia links

        Example:
            >>> engine = client.scan_engines.get_engine(6)
            >>> print(f"Engine: {engine['name']} ({engine['address']})")
            >>> print(f"Status: {engine['status']}")
        """
        return self._request('GET', f'scan_engines/{engine_id}')

    def update_engine(self, engine_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update configuration for an existing scan engine.

        Args:
            engine_id: The identifier of the scan engine
            **kwargs: Engine properties to update (name, address, port, etc.)

        Returns:
            Dictionary containing update confirmation and links

        Example:
            >>> result = client.scan_engines.update_engine(
            ...     engine_id=6,
            ...     name="Updated Engine Name"
            ... )
        """
        return self._request('PUT', f'scan_engines/{engine_id}', json=kwargs)

    def delete_engine(self, engine_id: int) -> Dict[str, Any]:
        """
        Delete a scan engine.

        Removes the scan engine from the system. The engine must not be
        actively scanning or assigned to any sites.

        Args:
            engine_id: The identifier of the scan engine

        Returns:
            Dictionary containing deletion confirmation and links

        Example:
            >>> result = client.scan_engines.delete_engine(6)
        """
        return self._request('DELETE', f'scan_engines/{engine_id}')

    # ==================== Scan Engine Sites ====================

    def get_sites(
        self,
        engine_id: int,
        page: int = 0,
        size: int = 10,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get the list of sites assigned to a scan engine.

        Args:
            engine_id: The identifier of the scan engine
            page: The page number to retrieve (zero-based)
            size: The number of records per page
            sort: Sort criteria in format 'property[,ASC|DESC]'

        Returns:
            Dictionary containing:
                - resources: List of site objects
                - page: Pagination information
                - links: Hypermedia links

        Example:
            >>> sites = client.scan_engines.get_sites(
            ...     engine_id=6,
            ...     size=50
            ... )
            >>> count = len(sites['resources'])
            >>> print(f"Engine assigned to {count} sites")
        """
        params: Dict[str, Any] = {'page': page, 'size': size}
        if sort:
            params['sort'] = sort
        return self._request(
            'GET',
            f'scan_engines/{engine_id}/sites',
            params=params
        )

    def get_scans(
        self,
        engine_id: int,
        page: int = 0,
        size: int = 10,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get scans that have been executed on a scan engine.

        Args:
            engine_id: The identifier of the scan engine
            page: The page number to retrieve (zero-based)
            size: The number of records per page
            sort: Sort criteria in format 'property[,ASC|DESC]'

        Returns:
            Dictionary containing:
                - resources: List of scan objects
                - page: Pagination information
                - links: Hypermedia links

        Example:
            >>> scans = client.scan_engines.get_scans(engine_id=6)
            >>> for scan in scans['resources']:
            ...     print(f"Scan {scan['id']}: {scan['status']}")
        """
        params: Dict[str, Any] = {'page': page, 'size': size}
        if sort:
            params['sort'] = sort
        return self._request(
            'GET',
            f'scan_engines/{engine_id}/scans',
            params=params
        )

    # ==================== Engine Pool Operations ====================

    def list_pools(self, **params) -> Dict[str, Any]:
        """
        List all engine pools available for scanning.

        Engine pools group multiple scan engines together for load balancing
        and high availability scanning.

        Args:
            **params: Optional query parameters (currently none supported by API)

        Returns:
            Dictionary containing:
                - resources: List of engine pool objects
                - links: Hypermedia links

        Example:
            >>> pools = client.scan_engines.list_pools()
            >>> for pool in pools['resources']:
            ...     n = len(pool['engines'])
            ...     print(f"{pool['name']}: {n} engines")
        """
        return self._request('GET', 'scan_engine_pools', params=params)

    def get_pool(self, pool_id: int) -> Dict[str, Any]:
        """
        Get details for a specific engine pool.

        Args:
            pool_id: The identifier of the engine pool

        Returns:
            Dictionary containing pool details including:
                - id: Pool identifier
                - name: Pool name
                - engines: List of engine IDs in the pool
                - sites: List of site IDs using this pool
                - links: Hypermedia links

        Example:
            >>> pool = client.scan_engines.get_pool(6)
            >>> print(f"Pool: {pool['name']}")
            >>> print(f"Engines: {pool['engines']}")
        """
        return self._request('GET', f'scan_engine_pools/{pool_id}')

    def create_pool(
        self,
        name: str,
        engine_ids: Optional[List[int]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new engine pool.

        Engine pools group multiple scan engines for load balancing and
        high availability.

        Args:
            name: Name for the engine pool
            engine_ids: List of scan engine IDs to include in the pool
            **kwargs: Additional pool properties

        Returns:
            Dictionary containing:
                - id: New pool identifier
                - links: Hypermedia links

        Example:
            >>> pool = client.scan_engines.create_pool(
            ...     name="Production Pool",
            ...     engine_ids=[1, 2, 3]
            ... )
            >>> print(f"Created pool {pool['id']}")
        """
        data = {'name': name, **kwargs}
        if engine_ids is not None:
            data['engines'] = engine_ids
        return self._request('POST', 'scan_engine_pools', json=data)

    def update_pool(self, pool_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update an existing engine pool.

        Args:
            pool_id: The identifier of the engine pool
            **kwargs: Pool properties to update (name, engines, etc.)

        Returns:
            Dictionary containing update confirmation and links

        Example:
            >>> result = client.scan_engines.update_pool(
            ...     pool_id=6,
            ...     name="Updated Pool Name"
            ... )
        """
        return self._request('PUT', f'scan_engine_pools/{pool_id}', json=kwargs)

    def delete_pool(self, pool_id: int) -> Dict[str, Any]:
        """
        Delete an engine pool.

        Args:
            pool_id: The identifier of the engine pool

        Returns:
            Dictionary containing deletion confirmation and links

        Example:
            >>> result = client.scan_engines.delete_pool(6)
        """
        return self._request('DELETE', f'scan_engine_pools/{pool_id}')

    def get_pool_engines(self, pool_id: int) -> Dict[str, Any]:
        """
        Get the list of engines in an engine pool.

        Args:
            pool_id: The identifier of the engine pool

        Returns:
            Dictionary containing:
                - resources: List of engine IDs in the pool
                - links: Hypermedia links

        Example:
            >>> engines = client.scan_engines.get_pool_engines(6)
            >>> print(f"Pool has {len(engines['resources'])} engines")
        """
        return self._request('GET', f'scan_engine_pools/{pool_id}/engines')

    def set_pool_engines(
        self,
        pool_id: int,
        engine_ids: List[int]
    ) -> Dict[str, Any]:
        """
        Set the engines in an engine pool.

        This replaces the current list of engines in the pool with the
        provided list.

        Args:
            pool_id: The identifier of the engine pool
            engine_ids: List of scan engine IDs to place in the pool

        Returns:
            Dictionary containing update confirmation and links

        Example:
            >>> result = client.scan_engines.set_pool_engines(
            ...     pool_id=6,
            ...     engine_ids=[1, 2, 3, 4]
            ... )
        """
        # The API expects a list directly, not wrapped in a dict
        # We need to pass it as JSON body despite type hint mismatch
        return self._request(
            'PUT',
            f'scan_engine_pools/{pool_id}/engines',
            json=engine_ids  # type: ignore[arg-type]
        )

    def get_engine_pools(self, engine_id: int) -> Dict[str, Any]:
        """
        Get the pools that a scan engine is assigned to.

        Args:
            engine_id: The identifier of the scan engine

        Returns:
            Dictionary containing:
                - resources: List of engine pool objects
                - links: Hypermedia links

        Example:
            >>> pools = client.scan_engines.get_engine_pools(engine_id=6)
            >>> for pool in pools['resources']:
            ...     print(f"Engine in pool: {pool['name']}")
        """
        return self._request(
            'GET',
            f'scan_engines/{engine_id}/scan_engine_pools'
        )

    # ==================== Shared Secret Operations ====================

    def delete_shared_secret(self) -> Dict[str, Any]:
        """
        Revoke the current valid shared secret for scan engines.

        The shared secret is used for pairing new scan engines with the
        console. Revoking it prevents new engines from being paired until
        a new secret is generated.

        Returns:
            Dictionary containing revocation confirmation and links

        Example:
            >>> result = client.scan_engines.delete_shared_secret()
        """
        return self._request('DELETE', 'scan_engines/shared_secret')

    # ==================== Helper Methods ====================

    def get_available_engines(self) -> List[Dict[str, Any]]:
        """
        Get list of all available (active) scan engines.

        Helper method that filters engines by status to return only
        those currently available for scanning. InsightVM engine status
        values are typically 'active', 'inactive', or 'unknown'.

        Returns:
            List of available scan engine objects with status 'active'

        Example:
            >>> engines = client.scan_engines.get_available_engines()
            >>> print(f"{len(engines)} engines available")
        """
        response = self.list()
        engines = response.get('resources', [])
        # Only include engines with 'active' status
        return [e for e in engines if e.get('status', '').lower() == 'active']

    def get_engine_summary(self, engine_id: int) -> Dict[str, Any]:
        """
        Get a summary of engine details including sites and pools.

        Helper method that combines engine details with site and pool
        assignments for a comprehensive view.

        Args:
            engine_id: The identifier of the scan engine

        Returns:
            Dictionary containing:
                - engine: Engine details
                - sites_count: Number of assigned sites
                - pools: List of assigned pools

        Example:
            >>> summary = client.scan_engines.get_engine_summary(6)
            >>> print(f"Engine: {summary['engine']['name']}")
            >>> print(f"Sites: {summary['sites_count']}")
            >>> print(f"Pools: {len(summary['pools'])}")
        """
        engine = self.get_engine(engine_id)
        sites = self.get_sites(engine_id, size=1)
        pools = self.get_engine_pools(engine_id)

        return {
            'engine': engine,
            'sites_count': sites.get('page', {}).get('totalResources', 0),
            'pools': pools.get('resources', [])
        }

    def assign_engine_to_pool(
        self,
        engine_id: int,
        pool_id: int
    ) -> Dict[str, Any]:
        """
        Assign a scan engine to an engine pool.

        Helper method that adds an engine to a pool's engine list.

        Args:
            engine_id: The identifier of the scan engine
            pool_id: The identifier of the engine pool

        Returns:
            Dictionary containing update confirmation and links

        Example:
            >>> result = client.scan_engines.assign_engine_to_pool(
            ...     engine_id=6,
            ...     pool_id=2
            ... )
        """
        # Get current engines in pool
        current = self.get_pool_engines(pool_id)
        current_engines = current.get('resources', [])

        # Add new engine if not already present
        if engine_id not in current_engines:
            current_engines.append(engine_id)

        # Update pool with new engine list
        return self.set_pool_engines(pool_id, current_engines)

    def remove_engine_from_pool(
        self,
        engine_id: int,
        pool_id: int
    ) -> Dict[str, Any]:
        """
        Remove a scan engine from an engine pool.

        Helper method that removes an engine from a pool's engine list.

        Args:
            engine_id: The identifier of the scan engine
            pool_id: The identifier of the engine pool

        Returns:
            Dictionary containing update confirmation and links

        Example:
            >>> result = client.scan_engines.remove_engine_from_pool(
            ...     engine_id=6,
            ...     pool_id=2
            ... )
        """
        # Get current engines in pool
        current = self.get_pool_engines(pool_id)
        current_engines = current.get('resources', [])

        # Remove engine if present
        if engine_id in current_engines:
            current_engines.remove(engine_id)

        # Update pool with new engine list
        return self.set_pool_engines(pool_id, current_engines)
