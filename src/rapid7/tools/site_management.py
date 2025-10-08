"""
Site management utility script.

This script provides custom helper functions for advanced site management
operations including filtering, bulk operations, and site analysis.

These are convenience functions built on top of the core SiteAPI and are
not part of the standardized API client.
"""

from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class SiteManagementTools:
    """
    Utility class for advanced site management operations.
    
    This class provides helper methods for filtering sites, performing
    bulk operations, and analyzing site configurations. These methods
    build on the core SiteAPI functionality.
    
    Example:
        >>> from rapid7 import InsightVMClient
        >>> from rapid7.tools.site_management import SiteManagementTools
        >>> 
        >>> client = InsightVMClient()
        >>> tools = SiteManagementTools(client.sites)
        >>> 
        >>> # Find empty sites
        >>> empty = tools.filter_empty_sites()
        >>> 
        >>> # Delete sites by pattern
        >>> result = tools.delete_by_pattern('sn_', dry_run=True)
    """
    
    def __init__(self, site_api):
        """
        Initialize site management tools.
        
        Args:
            site_api: SiteAPI instance from InsightVMClient
        """
        self.api = site_api
    
    def get_all_sites(self, batch_size: int = 500) -> List[Dict[str, Any]]:
        """
        Get all sites using automatic pagination.
        
        Args:
            batch_size: Number of sites per page (max 500)
        
        Returns:
            List of all site dictionaries
        """
        all_sites = []
        page = 0
        
        while True:
            response = self.api.list(page=page, size=batch_size)
            resources = response.get('resources', [])
            
            if not resources:
                break
            
            all_sites.extend(resources)
            
            page_info = response.get('page', {})
            total_pages = page_info.get('totalPages', 1)
            
            if page >= total_pages - 1:
                break
            
            page += 1
        
        return all_sites
    
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
            starts_with: Filter sites whose name starts with this
            ends_with: Filter sites whose name ends with this
            contains: Filter sites whose name contains this
            case_sensitive: Whether to match case-sensitively
        
        Returns:
            List of sites matching the pattern
        """
        all_sites = self.get_all_sites()
        filtered = []
        
        def _case(val):
            return val if case_sensitive or val is None else val.lower()
        
        for site in all_sites:
            name = site.get('name', '')
            name_cmp = _case(name)
            starts_cmp = _case(starts_with)
            ends_cmp = _case(ends_with)
            contains_cmp = _case(contains)
            
            if (
                (not starts_with or name_cmp.startswith(starts_cmp))
                and (not ends_with or name_cmp.endswith(ends_cmp))
                and (not contains or contains_cmp in name_cmp)
            ):
                filtered.append(site)
        
        return filtered
    
    def get_asset_count(self, site_id: int) -> int:
        """
        Get the number of assets in a site.
        
        Args:
            site_id: The site ID
        
        Returns:
            Number of assets in the site
        """
        assets_response = self.api.get_assets(site_id, page=0, size=1)
        page_info = assets_response.get('page', {})
        return page_info.get('totalResources', 0)
    
    def filter_empty_sites(self) -> List[Dict[str, Any]]:
        """
        Find all sites that have no assets.
        
        Returns:
            List of sites with zero assets
        """
        all_sites = self.get_all_sites()
        empty_sites = []
        
        for site in all_sites:
            site_id = site['id']
            try:
                asset_count = self.get_asset_count(site_id)
                if asset_count == 0:
                    site['asset_count'] = 0
                    empty_sites.append(site)
            except Exception as e:
                logger.warning(
                    f"Could not check assets for site {site_id}: {e}"
                )
        
        return empty_sites
    
    def filter_by_ids(self, site_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Filter sites by a list of site IDs.
        
        Args:
            site_ids: List of site IDs to retrieve
        
        Returns:
            List of sites matching the IDs
        """
        sites = []
        for site_id in site_ids:
            try:
                site = self.api.get_site(site_id)
                sites.append(site)
            except Exception as e:
                logger.warning(f"Could not retrieve site {site_id}: {e}")
        
        return sites
    
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
            dry_run: If True, only preview (default: True)
            continue_on_error: Continue if some deletions fail
        
        Returns:
            Dictionary with results including successes and failures
        """
        result: Dict[str, Any] = {
            'dry_run': dry_run,
            'total_requested': len(site_ids),
            'success_count': 0,
            'failure_count': 0,
            'successes': [],
            'failures': [],
            'preview': []
        }
        
        for site_id in site_ids:
            try:
                site = self.api.get_site(site_id)
                asset_count = self.get_asset_count(site_id)
                
                site_info = {
                    'id': site_id,
                    'name': site.get('name', 'Unknown'),
                    'asset_count': asset_count,
                    'description': site.get('description', '')
                }
                
                result['preview'].append(site_info)  # type: ignore
                
                if not dry_run:
                    try:
                        self.api.delete_site(site_id)
                        result['successes'].append(site_info)  # type: ignore
                        result['success_count'] += 1  # type: ignore
                        logger.info(
                            f"Deleted site {site_id}: {site.get('name')}"
                        )
                    except Exception as delete_error:
                        error_info = {
                            **site_info,
                            'error': str(delete_error)
                        }
                        result['failures'].append(error_info)  # type: ignore
                        result['failure_count'] += 1  # type: ignore
                        logger.error(
                            f"Failed to delete site {site_id}: "
                            f"{delete_error}"
                        )
                        
                        if not continue_on_error:
                            break
                            
            except Exception as e:
                error_info = {
                    'id': site_id,
                    'name': 'Could not retrieve',
                    'error': str(e)
                }
                result['failures'].append(error_info)  # type: ignore
                result['failure_count'] += 1  # type: ignore
                logger.error(f"Could not retrieve site {site_id}: {e}")
                
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
        """
        matching_sites = self.filter_by_name_pattern(contains=name_pattern)
        
        if empty_only:
            empty_site_ids = {s['id'] for s in self.filter_empty_sites()}
            matching_sites = [
                s for s in matching_sites if s['id'] in empty_site_ids
            ]
        
        site_ids = [s['id'] for s in matching_sites]
        
        return self.mass_delete(site_ids, dry_run=dry_run)
