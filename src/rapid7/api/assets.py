"""
Asset API operations for InsightVM.

This module provides comprehensive asset management operations including
listing, searching, retrieving, and managing assets in InsightVM.
"""

from typing import List, Dict, Optional, Any
from .base import BaseAPI


class AssetAPI(BaseAPI):
    """
    API client for InsightVM asset operations.

    This class provides methods for managing assets including
    listing, searching, and retrieving asset details.

    Example:
        >>> from src.rapid7.auth import InsightVMAuth
        >>> from src.rapid7.api.assets import AssetAPI
        >>>
        >>> auth = InsightVMAuth()
        >>> assets = AssetAPI(auth)
        >>>
        >>> # List assets with pagination
        >>> response = assets.list(page=0, size=100)
        >>>
        >>> # Get single asset
        >>> asset = assets.get(12345)
        >>>
        >>> # Get all assets (auto-pagination)
        >>> all_assets = assets.get_all()
        >>>
        >>> # Search assets
        >>> results = assets.search({
        ...     'filters': [{
        ...         'field': 'risk-score',
        ...         'operator': 'is-greater-than',
        ...         'value': 1000
        ...     }],
        ...     'match': 'all'
        ... })
    """

    def list(
        self,
        page: int = 0,
        size: int = 500,
        sort: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        List assets with pagination.

        Args:
            page: Page number (0-indexed)
            size: Number of assets per page (max 500)
            sort: List of sort criteria (e.g., ['risk-score:desc'])
            filters: Additional filter parameters

        Returns:
            Dictionary containing assets and pagination info

        Example:
            >>> response = assets.list(page=0, size=100)
            >>> for asset in response['resources']:
            ...     print(asset['id'], asset['ip'])
        """
        params = {
            'page': page,
            'size': min(size, 500)  # API max is 500
        }

        if sort:
            params['sort'] = ','.join(sort)

        if filters:
            params.update(filters)

        response = self.get('assets', params=params)
        return response.json()

    def get_asset(self, asset_id: int) -> Dict[str, Any]:
        """
        Get a single asset by ID.

        Args:
            asset_id: The asset ID

        Returns:
            Dictionary containing asset details

        Example:
            >>> asset = assets.get_asset(12345)
            >>> print(asset['hostName'], asset['ip'])
        """
        response = self.get(f'assets/{asset_id}')
        return response.json()

    def search(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for assets using criteria.

        Args:
            criteria: Search criteria with filters and match type

        Returns:
            Dictionary containing matching assets

        Example:
            >>> results = assets.search({
            ...     'filters': [{
            ...         'field': 'risk-score',
            ...         'operator': 'is-greater-than',
            ...         'value': 5000
            ...     }],
            ...     'match': 'all'
            ... })
        """
        response = self.post('assets/search', json=criteria)
        return response.json()

    def get_all(self, batch_size: int = 500) -> List[Dict[str, Any]]:
        """
        Get all assets using automatic pagination.

        This method handles pagination automatically and returns all assets.
        Use with caution in environments with many assets as this can be
        memory-intensive and time-consuming.

        Args:
            batch_size: Number of assets to fetch per page (max 500)

        Returns:
            List of all asset dictionaries

        Example:
            >>> all_assets = assets.get_all()
            >>> print(f"Total assets: {len(all_assets)}")
        """
        all_assets = []
        page = 0

        while True:
            response = self.list(page=page, size=batch_size)
            resources = response.get('resources', [])

            if not resources:
                break

            all_assets.extend(resources)

            # Check if there are more pages
            page_info = response.get('page', {})
            total_pages = page_info.get('totalPages', 1)

            if page >= total_pages - 1:
                break

            page += 1

        return all_assets

    def get_vulnerabilities(
        self,
        asset_id: int,
        page: int = 0,
        size: int = 500
    ) -> Dict[str, Any]:
        """
        Get vulnerabilities for a specific asset.

        Args:
            asset_id: The asset ID
            page: Page number (0-indexed)
            size: Number of vulnerabilities per page

        Returns:
            Dictionary containing vulnerabilities

        Example:
            >>> vulns = assets.get_vulnerabilities(12345)
            >>> for vuln in vulns['resources']:
            ...     print(vuln['id'], vuln['title'])
        """
        params = {'page': page, 'size': size}
        response = self.get(f'assets/{asset_id}/vulnerabilities', params=params)
        return response.json()

    def get_software(
        self,
        asset_id: int,
        page: int = 0,
        size: int = 500
    ) -> Dict[str, Any]:
        """
        Get software installed on a specific asset.

        Args:
            asset_id: The asset ID
            page: Page number (0-indexed)
            size: Number of software items per page

        Returns:
            Dictionary containing software information

        Example:
            >>> software = assets.get_software(12345)
            >>> for sw in software['resources']:
            ...     print(sw['product'], sw['version'])
        """
        params = {'page': page, 'size': size}
        response = self.get(f'assets/{asset_id}/software', params=params)
        return response.json()

    def get_tags(self, asset_id: int) -> Dict[str, Any]:
        """
        Get tags assigned to a specific asset.

        Args:
            asset_id: The asset ID

        Returns:
            Dictionary containing tag information

        Example:
            >>> tags = assets.get_tags(12345)
            >>> for tag in tags['resources']:
            ...     print(tag['name'])
        """
        response = self.get(f'assets/{asset_id}/tags')
        return response.json()

    def add_tag(self, asset_id: int, tag_id: int) -> Dict[str, Any]:
        """
        Add a tag to an asset.

        Args:
            asset_id: The asset ID
            tag_id: The tag ID to add

        Returns:
            Response confirming the operation

        Example:
            >>> result = assets.add_tag(12345, 67)
        """
        response = self.put(f'assets/{asset_id}/tags/{tag_id}')
        return response.json()

    def remove_tag(self, asset_id: int, tag_id: int) -> None:
        """
        Remove a tag from an asset.

        Args:
            asset_id: The asset ID
            tag_id: The tag ID to remove

        Example:
            >>> assets.remove_tag(12345, 67)
        """
        self.delete(f'assets/{asset_id}/tags/{tag_id}')
