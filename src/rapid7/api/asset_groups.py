"""
Asset Group API operations for InsightVM.

This module provides asset group management operations including
creating, updating, deleting, and managing dynamic asset groups.
"""

from typing import Dict, Optional, Any
from .base import BaseAPI


class AssetGroupAPI(BaseAPI):
    """
    API client for InsightVM asset group operations.
    
    This class provides methods for managing asset groups including
    listing, creating, updating, and deleting groups.
    
    Example:
        >>> from src.rapid7.auth import InsightVMAuth
        >>> from src.rapid7.api.asset_groups import AssetGroupAPI
        >>> 
        >>> auth = InsightVMAuth()
        >>> groups = AssetGroupAPI(auth)
        >>> 
        >>> # List all asset groups
        >>> all_groups = groups.list()
        >>> 
        >>> # Create high-risk asset group
        >>> high_risk = groups.create_high_risk()
        >>> 
        >>> # Create custom group
        >>> custom = groups.create(
        ...     name="Production Servers",
        ...     description="All production servers",
        ...     search_criteria={
        ...         'filters': [{
        ...             'field': 'host-name',
        ...             'operator': 'contains',
        ...             'value': 'prod'
        ...         }],
        ...         'match': 'all'
        ...     }
        ... )
    """
    
    def list(self) -> Dict[str, Any]:
        """
        List all asset groups.
        
        Returns:
            Dictionary containing all asset groups
            
        Example:
            >>> groups_list = groups.list()
            >>> for group in groups_list['resources']:
            ...     print(group['id'], group['name'])
        """
        response = self.get('asset_groups')
        return response.json()
    
    def get_group(self, group_id: int) -> Dict[str, Any]:
        """
        Get a specific asset group by ID.
        
        Args:
            group_id: The asset group ID
        
        Returns:
            Dictionary containing asset group details
            
        Example:
            >>> group = groups.get_group(42)
            >>> print(group['name'], len(group.get('assets', [])))
        """
        response = self.get(f'asset_groups/{group_id}')
        return response.json()
    
    def create(
        self,
        name: str,
        description: Optional[str] = None,
        search_criteria: Optional[Dict[str, Any]] = None,
        group_type: str = 'dynamic'
    ) -> Dict[str, Any]:
        """
        Create a new asset group.
        
        Args:
            name: Name of the asset group
            description: Description of the asset group
            search_criteria: Search criteria for dynamic groups
            group_type: Type of group ('dynamic' or 'static')
        
        Returns:
            Dictionary containing the created group info with ID
            
        Example:
            >>> group = groups.create(
            ...     name="Critical Assets",
            ...     description="Assets with critical vulnerabilities",
            ...     search_criteria={
            ...         'filters': [{
            ...             'field': 'cvss-score',
            ...             'operator': 'is-greater-than',
            ...             'value': 9.0
            ...         }],
            ...         'match': 'all'
            ...     }
            ... )
            >>> print(f"Created group ID: {group['id']}")
        """
        payload = {
            'name': name,
            'type': group_type,
        }
        
        if description:
            payload['description'] = description
        
        if search_criteria:
            payload['searchCriteria'] = search_criteria
        
        response = self.post('asset_groups', json=payload)
        return response.json()
    
    def create_high_risk(
        self,
        name: str = "High Risk Assets",
        threshold: int = 25000,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a high-risk asset group based on risk score.
        
        This is a convenience method for creating a common type of
        asset group that identifies assets above a risk threshold.
        
        Args:
            name: Name for the asset group
            threshold: Minimum risk score (default: 25000)
            description: Optional description
        
        Returns:
            Dictionary containing the created group info
            
        Example:
            >>> high_risk = groups.create_high_risk(
            ...     name="Critical Risk Assets",
            ...     threshold=50000
            ... )
        """
        if description is None:
            description = (
                f"Assets with risk score greater than {threshold} "
                "requiring immediate remediation."
            )
        
        criteria = {
            'filters': [{
                'field': 'risk-score',
                'operator': 'is-greater-than',
                'value': threshold
            }],
            'match': 'all'
        }
        
        return self.create(
            name=name,
            description=description,
            search_criteria=criteria
        )
    
    def update(
        self,
        group_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        search_criteria: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing asset group.
        
        Args:
            group_id: The asset group ID
            name: New name (optional)
            description: New description (optional)
            search_criteria: New search criteria (optional)
        
        Returns:
            Dictionary confirming the update
            
        Example:
            >>> groups.update(
            ...     group_id=42,
            ...     description="Updated description"
            ... )
        """
        # Get current group to preserve unmodified fields
        current = self.get_group(group_id)
        
        payload = {
            'name': name or current.get('name'),
            'type': current.get('type', 'dynamic'),
        }
        
        if description is not None:
            payload['description'] = description
        elif 'description' in current:
            payload['description'] = current['description']
        
        if search_criteria is not None:
            payload['searchCriteria'] = search_criteria
        elif 'searchCriteria' in current:
            payload['searchCriteria'] = current['searchCriteria']
        
        response = self.put(f'asset_groups/{group_id}', json=payload)
        return response.json()
    
    def delete_group(self, group_id: int) -> None:
        """
        Delete an asset group.
        
        Args:
            group_id: The asset group ID to delete
            
        Example:
            >>> groups.delete_group(42)
        """
        self.delete(f'asset_groups/{group_id}')
    
    def get_assets(
        self,
        group_id: int,
        page: int = 0,
        size: int = 500
    ) -> Dict[str, Any]:
        """
        Get assets belonging to a specific group.
        
        Args:
            group_id: The asset group ID
            page: Page number (0-indexed)
            size: Number of assets per page
        
        Returns:
            Dictionary containing assets in the group
            
        Example:
            >>> assets = groups.get_assets(42)
            >>> for asset in assets['resources']:
            ...     print(asset['id'], asset['ip'])
        """
        params = {'page': page, 'size': size}
        response = self.get(f'asset_groups/{group_id}/assets', params=params)
        return response.json()
    
    def add_asset(self, group_id: int, asset_id: int) -> Dict[str, Any]:
        """
        Add an asset to a static asset group.
        
        Note: This only works for static groups, not dynamic groups.
        
        Args:
            group_id: The asset group ID
            asset_id: The asset ID to add
        
        Returns:
            Dictionary confirming the operation
            
        Example:
            >>> groups.add_asset(group_id=42, asset_id=12345)
        """
        response = self.put(f'asset_groups/{group_id}/assets/{asset_id}')
        return response.json()
    
    def remove_asset(self, group_id: int, asset_id: int) -> None:
        """
        Remove an asset from a static asset group.
        
        Note: This only works for static groups, not dynamic groups.
        
        Args:
            group_id: The asset group ID
            asset_id: The asset ID to remove
            
        Example:
            >>> groups.remove_asset(group_id=42, asset_id=12345)
        """
        self.delete(f'asset_groups/{group_id}/assets/{asset_id}')
    
    def search_tags(self, group_id: int) -> Dict[str, Any]:
        """
        Get search criteria tags for an asset group.
        
        Args:
            group_id: The asset group ID
        
        Returns:
            Dictionary containing tag search criteria
            
        Example:
            >>> tags = groups.search_tags(42)
        """
        response = self.get(f'asset_groups/{group_id}/tags')
        return response.json()
