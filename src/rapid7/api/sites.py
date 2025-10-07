"""
Site API operations for InsightVM.

This module provides comprehensive site management operations including
listing, searching, creating, updating, and deleting sites. It also includes
smart filtering and mass operations with safety features.
"""

from typing import List, Dict, Optional, Any
import logging
from .base import BaseAPI


logger = logging.getLogger(__name__)


class SiteAPI(BaseAPI):
    """
    API client for InsightVM site operations.
    
    This class provides methods for managing sites including CRUD operations,
    smart filtering, and mass operations with validation.
    
    Example:
        >>> from src.rapid7.auth import InsightVMAuth
        >>> from src.rapid7.api.sites import SiteAPI
        >>> 
        >>> auth = InsightVMAuth()
        >>> sites = SiteAPI(auth)
        >>> 
        >>> # List sites with pagination
        >>> response = sites.list(page=0, size=100)
        >>> 
        >>> # Get single site
        >>> site = sites.get_site(123)
        >>> 
        >>> # Filter sites by name pattern
        >>> filtered = sites.filter_by_name_pattern(starts_with='sn_')
        >>> 
        >>> # Get empty sites (no assets)
        >>> empty_sites = sites.filter_empty_sites()
        >>> 
        >>> # Mass delete with preview
        >>> result = sites.mass_delete([1, 2, 3], dry_run=True)
    """
    
    def list(
        self,
        page: int = 0,
        size: int = 500,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        List sites with pagination.
        
        Args:
            page: Page number (0-indexed)
            size: Number of sites per page (max 500)
            sort: List of sort criteria (e.g., ['name:asc', 'id:desc'])
        
        Returns:
            Dictionary containing sites and pagination info
            
        Example:
            >>> response = sites.list(page=0, size=100)
            >>> for site in response['resources']:
            ...     print(site['id'], site['name'])
        """
        params = {
            'page': page,
            'size': min(size, 500)  # API max is 500
        }
        
        if sort:
            params['sort'] = ','.join(sort)
        
        response = self.get('sites', params=params)
        return response.json()
    
    def get_all(self, batch_size: int = 500) -> List[Dict[str, Any]]:
        """
        Get all sites using automatic pagination.
        
        This method handles pagination automatically and returns all sites.
        
        Args:
            batch_size: Number of sites to fetch per page (max 500)
        
        Returns:
            List of all site dictionaries
            
        Example:
            >>> all_sites = sites.get_all()
            >>> print(f"Total sites: {len(all_sites)}")
        """
        all_sites = []
        page = 0
        
        while True:
            response = self.list(page=page, size=batch_size)
            resources = response.get('resources', [])
            
            if not resources:
                break
            
            all_sites.extend(resources)
            
            # Check if there are more pages
            page_info = response.get('page', {})
            total_pages = page_info.get('totalPages', 1)
            
            if page >= total_pages - 1:
                break
            
            page += 1
        
        return all_sites
    
    def get_site(self, site_id: int) -> Dict[str, Any]:
        """
        Get a single site by ID.
        
        Args:
            site_id: The site ID
        
        Returns:
            Dictionary containing site details
            
        Example:
            >>> site = sites.get_site(123)
            >>> print(site['name'], site['type'])
        """
        response = self.get(f'sites/{site_id}')
        return response.json()
    
    def create(
        self,
        name: str,
        description: Optional[str] = None,
        scan_engine_id: Optional[int] = None,
        scan_template_id: Optional[str] = None,
        importance: str = "normal",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new site.
        
        Args:
            name: Site name (required)
            description: Site description
            scan_engine_id: Scan engine ID to use
            scan_template_id: Scan template ID to use
            importance: Site importance (low, normal, high)
            **kwargs: Additional site properties
        
        Returns:
            Created site details including ID
            
        Example:
            >>> site = sites.create(
            ...     name="Production Servers",
            ...     description="Critical production infrastructure",
            ...     importance="high"
            ... )
            >>> print(f"Created site: {site['id']}")
        """
        payload = {
            'name': name,
            'importance': importance
        }
        
        if description:
            payload['description'] = description
        if scan_engine_id:
            payload['engineId'] = scan_engine_id
        if scan_template_id:
            payload['scanTemplateId'] = scan_template_id
        
        # Add any additional properties
        payload.update(kwargs)
        
        response = self.post('sites', json=payload)
        return response.json()
    
    def update(
        self,
        site_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        importance: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing site.
        
        Args:
            site_id: The site ID to update
            name: New site name
            description: New site description
            importance: New importance level (low, normal, high)
            **kwargs: Additional properties to update
        
        Returns:
            Updated site details
            
        Example:
            >>> site = sites.update(
            ...     123,
            ...     name="Updated Name",
            ...     importance="high"
            ... )
        """
        # First get current site data
        current_site = self.get_site(site_id)
        
        # Update with new values
        if name:
            current_site['name'] = name
        if description is not None:
            current_site['description'] = description
        if importance:
            current_site['importance'] = importance
        
        # Add any additional updates
        current_site.update(kwargs)
        
        response = self.put(f'sites/{site_id}', json=current_site)
        return response.json()
    
    def delete_site(self, site_id: int) -> None:
        """
        Delete a site by ID.
        
        Args:
            site_id: The site ID to delete
            
        Example:
            >>> sites.delete_site(123)
        """
        self.delete(f'sites/{site_id}')
    
    def get_assets(
        self,
        site_id: int,
        page: int = 0,
        size: int = 500
    ) -> Dict[str, Any]:
        """
        Get assets for a specific site.
        
        Args:
            site_id: The site ID
            page: Page number (0-indexed)
            size: Number of assets per page
        
        Returns:
            Dictionary containing assets in the site
            
        Example:
            >>> assets = sites.get_assets(123)
            >>> for asset in assets['resources']:
            ...     print(asset['ip'], asset['hostName'])
        """
        params = {'page': page, 'size': size}
        response = self.get(f'sites/{site_id}/assets', params=params)
        return response.json()
    
    def get_asset_count(self, site_id: int) -> int:
        """
        Get the number of assets in a site.
        
        Args:
            site_id: The site ID
        
        Returns:
            Number of assets in the site
            
        Example:
            >>> count = sites.get_asset_count(123)
            >>> print(f"Site has {count} assets")
        """
        assets_response = self.get_assets(site_id, page=0, size=1)
        page_info = assets_response.get('page', {})
        return page_info.get('totalResources', 0)
    
    # Smart Filtering Methods
    
    def filter_by_name_pattern(
        self,
        starts_with: Optional[str] = None,
        ends_with: Optional[str] = None,
        contains: Optional[str] = None,
        case_sensitive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Filter sites by name patterns.
        
        Args:
            starts_with: Filter sites whose name starts with this string
            ends_with: Filter sites whose name ends with this string
            contains: Filter sites whose name contains this string
            case_sensitive: Whether to perform case-sensitive matching
        
        Returns:
            List of sites matching the pattern
            
        Example:
            >>> # Get all sites starting with 'sn_'
            >>> sn_sites = sites.filter_by_name_pattern(starts_with='sn_')
            >>> 
            >>> # Get all sites containing 'prod'
            >>> prod_sites = sites.filter_by_name_pattern(contains='prod')
        """
        all_sites = self.get_all()
        filtered = []
        
        # Helper function for case conversion
        def _case(val):
            return val if case_sensitive or val is None else val.lower()
        
        for site in all_sites:
            name = site.get('name', '')
            name_cmp = _case(name)
            starts_cmp = _case(starts_with)
            ends_cmp = _case(ends_with)
            contains_cmp = _case(contains)
            
            # Check all conditions in a single boolean expression
            if (
                (not starts_with or name_cmp.startswith(starts_cmp))
                and (not ends_with or name_cmp.endswith(ends_cmp))
                and (not contains or contains_cmp in name_cmp)
            ):
                filtered.append(site)
        
        return filtered
    
    def filter_by_ids(self, site_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Filter sites by a list of site IDs.
        
        Args:
            site_ids: List of site IDs to retrieve
        
        Returns:
            List of sites matching the IDs
            
        Example:
            >>> selected_sites = sites.filter_by_ids([1, 5, 10, 15])
        """
        sites = []
        for site_id in site_ids:
            try:
                site = self.get_site(site_id)
                sites.append(site)
            except Exception as e:
                logger.warning(f"Could not retrieve site {site_id}: {str(e)}")
        
        return sites
    
    def filter_empty_sites(self) -> List[Dict[str, Any]]:
        """
        Find all sites that have no assets.
        
        Returns:
            List of sites with zero assets
            
        Example:
            >>> empty_sites = sites.filter_empty_sites()
            >>> print(f"Found {len(empty_sites)} empty sites")
        """
        all_sites = self.get_all()
        empty_sites = []
        
        for site in all_sites:
            site_id = site['id']
            try:
                asset_count = self.get_asset_count(site_id)
                if asset_count == 0:
                    site['asset_count'] = 0
                    empty_sites.append(site)
            except Exception as e:
                logger.warning(f"Could not check assets for site {site_id}: {str(e)}")
        
        return empty_sites
    
    def filter_sites(
        self,
        name_pattern: Optional[str] = None,
        site_ids: Optional[List[int]] = None,
        empty_only: bool = False,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Combined filtering method with multiple criteria.
        
        Args:
            name_pattern: Filter by name (partial match)
            site_ids: Filter by specific site IDs
            empty_only: Only return sites with no assets
            **kwargs: Additional filter criteria
        
        Returns:
            List of sites matching all criteria
            
        Example:
            >>> # Get empty sites starting with 'sn_'
            >>> filtered = sites.filter_sites(
            ...     name_pattern='sn_',
            ...     empty_only=True
            ... )
        """
        # Start with all sites or specified IDs
        if site_ids:
            filtered_sites = self.filter_by_ids(site_ids)
        else:
            filtered_sites = self.get_all()
        
        # Apply name pattern filter using filter_by_name_pattern
        # for consistency
        if name_pattern:
            name_pattern_sites = self.filter_by_name_pattern(
                contains=name_pattern
            )
            name_pattern_site_ids = {s['id'] for s in name_pattern_sites}
            filtered_sites = [
                s for s in filtered_sites
                if s['id'] in name_pattern_site_ids
            ]
        
        # Apply empty sites filter
        if empty_only:
            empty_site_ids = {
                s['id'] for s in self.filter_empty_sites()
            }
            filtered_sites = [
                s for s in filtered_sites if s['id'] in empty_site_ids
            ]
        
        return filtered_sites
    
    # Mass Operations
    
    def mass_delete(
        self,
        site_ids: List[int],
        dry_run: bool = True,
        continue_on_error: bool = True
    ) -> Dict[str, Any]:
        """
        Delete multiple sites with validation and error handling.
        
        Args:
            site_ids: List of site IDs to delete
            dry_run: If True, only preview what would be deleted (default: True)
            continue_on_error: If True, continue deleting even if some fail
        
        Returns:
            Dictionary with results including successes, failures, and preview
            
        Example:
            >>> # Preview deletion
            >>> preview = sites.mass_delete([1, 2, 3], dry_run=True)
            >>> print(f"Would delete {len(preview['preview'])} sites")
            >>> 
            >>> # Actually delete
            >>> result = sites.mass_delete([1, 2, 3], dry_run=False)
            >>> print(f"Deleted: {result['success_count']}")
            >>> print(f"Failed: {result['failure_count']}")
        """
        result = {
            'dry_run': dry_run,
            'total_requested': len(site_ids),
            'success_count': 0,
            'failure_count': 0,
            'successes': [],
            'failures': [],
            'preview': []
        }
        
        # Get site details for preview
        for site_id in site_ids:
            try:
                site = self.get_site(site_id)
                asset_count = self.get_asset_count(site_id)
                
                site_info = {
                    'id': site_id,
                    'name': site.get('name', 'Unknown'),
                    'asset_count': asset_count,
                    'description': site.get('description', '')
                }
                
                result['preview'].append(site_info)
                
                # If not dry run, actually delete
                if not dry_run:
                    try:
                        self.delete_site(site_id)
                        result['successes'].append(site_info)
                        result['success_count'] += 1
                        logger.info(
                            f"Deleted site {site_id}: {site.get('name')}"
                        )
                    except Exception as delete_error:
                        error_info = {
                            **site_info,
                            'error': str(delete_error)
                        }
                        result['failures'].append(error_info)
                        result['failure_count'] += 1
                        logger.error(
                            f"Failed to delete site {site_id}: "
                            f"{str(delete_error)}"
                        )
                        
                        if not continue_on_error:
                            break
                            
            except Exception as e:
                error_info = {
                    'id': site_id,
                    'name': 'Could not retrieve',
                    'error': str(e)
                }
                result['failures'].append(error_info)
                result['failure_count'] += 1
                logger.error(f"Could not retrieve site {site_id}: {str(e)}")
                
                if not continue_on_error and not dry_run:
                    break
        
        return result
    
    def delete_by_pattern(
        self,
        name_pattern: str,
        dry_run: bool = True,
        empty_only: bool = False
    ) -> Dict[str, Any]:
        """
        Delete sites matching a name pattern.
        
        Args:
            name_pattern: Name pattern to match
            dry_run: If True, only preview (default: True)
            empty_only: Only delete sites with no assets
        
        Returns:
            Dictionary with deletion results
            
        Example:
            >>> # Preview deletion of empty sites starting with 'sn_'
            >>> result = sites.delete_by_pattern(
            ...     name_pattern='sn_',
            ...     empty_only=True,
            ...     dry_run=True
            ... )
        """
        # Get sites matching pattern
        matching_sites = self.filter_sites(
            name_pattern=name_pattern,
            empty_only=empty_only
        )
        
        # Extract site IDs
        site_ids = [s['id'] for s in matching_sites]
        
        # Perform mass delete
        return self.mass_delete(site_ids, dry_run=dry_run)
    
    def get_scan_template(self, site_id: int) -> Dict[str, Any]:
        """
        Get the scan template for a site.
        
        Args:
            site_id: The site ID
        
        Returns:
            Scan template details
            
        Example:
            >>> template = sites.get_scan_template(123)
            >>> print(template['name'])
        """
        response = self.get(f'sites/{site_id}/scan_template')
        return response.json()
    
    def get_scan_engine(self, site_id: int) -> Dict[str, Any]:
        """
        Get the scan engine for a site.
        
        Args:
            site_id: The site ID
        
        Returns:
            Scan engine details
            
        Example:
            >>> engine = sites.get_scan_engine(123)
            >>> print(engine['name'])
        """
        response = self.get(f'sites/{site_id}/scan_engine')
        return response.json()
