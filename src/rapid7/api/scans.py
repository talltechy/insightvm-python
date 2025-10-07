"""
Rapid7 InsightVM Scans API Module

This module provides a comprehensive interface for managing scans in InsightVM.
It supports listing, retrieving, starting, stopping, pausing, and resuming scans,
as well as monitoring scan status and retrieving scan history.

Example:
    ```python
    from rapid7 import InsightVMClient
    
    # Create client
    client = InsightVMClient()
    
    # List all scans
    scans = client.scans.list()
    
    # Start a scan for a site
    scan_id = client.scans.start_site_scan(
        site_id=123,
        scan_name="Security Audit",
        scan_template_id="full-audit-without-web-spider"
    )
    
    # Monitor scan status
    scan = client.scans.get_scan(scan_id)
    print(f"Status: {scan['status']}")
    
    # Stop a running scan
    client.scans.stop_scan(scan_id)
    ```
"""

from typing import Dict, List, Optional, Any
import time
from .base import BaseAPI


class ScansAPI(BaseAPI):
    """
    API client for InsightVM Scans operations.
    
    This class provides methods for managing vulnerability scans including:
    - Listing and retrieving scans
    - Starting scans (adhoc and site-based)
    - Controlling scan execution (start, stop, pause, resume)
    - Monitoring scan status and progress
    - Retrieving scan history and results
    
    All methods follow the BaseAPI pattern and handle authentication,
    SSL verification, and error handling automatically.
    """
    
    def list(
        self,
        active: Optional[bool] = None,
        page: int = 0,
        size: int = 500,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        List all scans.
        
        Returns a paginated list of scans with support for filtering by
        active status and sorting.
        
        Args:
            active: If True, return only running scans. If False, return
                   only completed scans. If None, return all scans.
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
            sort: List of sort criteria in format "property[,ASC|DESC]"
                 Example: ["startTime,DESC", "scanName,ASC"]
        
        Returns:
            Dictionary containing:
                - resources: List of scan objects
                - page: Pagination metadata (number, size,
                  totalPages, totalResources)
                - links: HATEOAS links
        
        Example:
            ```python
            # Get all active scans
            active_scans = client.scans.list(active=True)
            
            # Get completed scans sorted by end time
            completed = client.scans.list(
                active=False,
                sort=["endTime,DESC"]
            )
            ```
        """
        params: Dict[str, Any] = {
            'page': page,
            'size': size
        }
        
        if active is not None:
            params['active'] = str(active).lower()
        
        if sort:
            params['sort'] = sort
        
        return self._request('GET', 'scans', params=params)
    
    def get_scan(self, scan_id: int) -> Dict[str, Any]:
        """
        Get details for a specific scan.
        
        Retrieves comprehensive information about a scan including its status,
        progress, assets scanned, vulnerabilities found, and timing information.
        
        Args:
            scan_id: The unique identifier of the scan
        
        Returns:
            Dictionary containing scan details:
                - id: Scan identifier
                - scanName: Name of the scan
                - scanType: Type of scan
                - status: Current status (running, finished,
                  stopped, etc.)
                - startTime: When the scan started
                - endTime: When the scan completed (if finished)
                - duration: Scan duration
                - assets: Number of assets scanned
                - vulnerabilities: Vulnerability counts by severity
                - engineId: ID of scan engine used
                - engineName: Name of scan engine
                - message: Status message
                - links: HATEOAS links
        
        Raises:
            requests.exceptions.HTTPError: If scan not found (404)
                or access denied
        
        Example:
            ```python
            scan = client.scans.get_scan(12345)
            print(f"Status: {scan['status']}")
            print(f"Assets: {scan['assets']}")
            print(f"Critical: {scan['vulnerabilities']['critical']}")
            ```
        """
        return self._request('GET', f'scans/{scan_id}')
    
    def get_site_scans(
        self,
        site_id: int,
        active: Optional[bool] = None,
        page: int = 0,
        size: int = 500,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get all scans for a specific site.
        
        Retrieves a paginated list of scans associated with a site, with
        optional filtering by active status.
        
        Args:
            site_id: The unique identifier of the site
            active: If True, return only running scans. If False, return
                   only completed scans. If None, return all scans.
            page: Zero-based page index to retrieve (default: 0)
            size: Number of records per page (default: 500, max: 500)
            sort: List of sort criteria in format "property[,ASC|DESC]"
        
        Returns:
            Dictionary containing:
                - resources: List of scan objects for the site
                - page: Pagination metadata
                - links: HATEOAS links
        
        Example:
            ```python
            # Get all scans for site 42
            scans = client.scans.get_site_scans(42)
            
            # Get active scans for site
            active = client.scans.get_site_scans(
                site_id=42,
                active=True
            )
            ```
        """
        params: Dict[str, Any] = {
            'page': page,
            'size': size
        }
        
        if active is not None:
            params['active'] = str(active).lower()
        
        if sort:
            params['sort'] = sort
        
        return self._request(
            'GET', f'sites/{site_id}/scans', params=params
        )
    
    def start_site_scan(
        self,
        site_id: int,
        scan_name: Optional[str] = None,
        scan_template_id: Optional[str] = None,
        hosts: Optional[List[str]] = None,
        asset_group_ids: Optional[List[int]] = None,
        engine_id: Optional[int] = None,
        override_blackout: bool = False
    ) -> int:
        """
        Start a new scan for a site.
        
        Initiates a scan on the specified site with optional customization
        of hosts, scan template, and scan engine.
        
        Args:
            site_id: The unique identifier of the site to scan
            scan_name: Optional name for the scan. If not provided,
                      a default name will be generated.
            scan_template_id: Optional scan template ID to use.
                            Common templates:
                            - "full-audit-without-web-spider"
                            - "full-audit"
                            - "discovery"
                            - "exhaustive"
            hosts: Optional list of specific hosts to scan
                  (IP addresses or hostnames).
                  If not provided, all site assets will be scanned.
            asset_group_ids: Optional list of asset group IDs to include
                            in scan
            engine_id: Optional scan engine ID to use. If not provided,
                      the site's default engine will be used.
            override_blackout: If True, override scan blackout window
                              restrictions (default: False)
        
        Returns:
            Integer scan ID of the newly started scan
        
        Raises:
            requests.exceptions.HTTPError: If site not found,
                insufficient permissions, or service unavailable
        
        Example:
            ```python
            # Start scan with default settings
            scan_id = client.scans.start_site_scan(site_id=42)
            
            # Start customized scan
            scan_id = client.scans.start_site_scan(
                site_id=42,
                scan_name="Monthly Security Audit",
                scan_template_id="full-audit-without-web-spider",
                hosts=["192.168.1.10", "192.168.1.20"],
                override_blackout=True
            )
            print(f"Started scan {scan_id}")
            ```
        """
        # Build adhoc scan configuration
        adhoc_scan: Dict[str, Any] = {}
        
        if scan_name:
            adhoc_scan['name'] = scan_name
        
        if scan_template_id:
            adhoc_scan['templateId'] = scan_template_id
        
        if hosts:
            adhoc_scan['hosts'] = hosts
        
        if asset_group_ids:
            adhoc_scan['assetGroupIds'] = asset_group_ids
        
        if engine_id:
            adhoc_scan['engineId'] = engine_id
        
        # Build query parameters
        params: Dict[str, str] = {}
        if override_blackout:
            params['overrideBlackout'] = 'true'
        
        # Start the scan
        response = self._request(
            'POST',
            f'sites/{site_id}/scans',
            json=adhoc_scan if adhoc_scan else None,
            params=params if params else None
        )
        
        return response['id']
    
    def stop_scan(self, scan_id: int) -> Dict[str, Any]:
        """
        Stop a running or paused scan.
        
        Stops the specified scan. The scan must be in running or paused state.
        
        Args:
            scan_id: The unique identifier of the scan to stop
        
        Returns:
            Dictionary with links to the scan resource
        
        Raises:
            requests.exceptions.HTTPError: If scan not found,
                already stopped, or not in a stoppable state (400)
        
        Example:
            ```python
            # Stop a running scan
            result = client.scans.stop_scan(12345)
            ```
        """
        return self._request('POST', f'scans/{scan_id}/stop')
    
    def pause_scan(self, scan_id: int) -> Dict[str, Any]:
        """
        Pause a running scan.
        
        Pauses the specified scan. The scan must be in running state.
        
        Args:
            scan_id: The unique identifier of the scan to pause
        
        Returns:
            Dictionary with links to the scan resource
        
        Raises:
            requests.exceptions.HTTPError: If scan not found or not in
                running state (400)
        
        Example:
            ```python
            # Pause a running scan
            result = client.scans.pause_scan(12345)
            ```
        """
        return self._request('POST', f'scans/{scan_id}/pause')
    
    def resume_scan(self, scan_id: int) -> Dict[str, Any]:
        """
        Resume a paused scan.
        
        Resumes the specified scan. The scan must be in paused state.
        
        Args:
            scan_id: The unique identifier of the scan to resume
        
        Returns:
            Dictionary with links to the scan resource
        
        Raises:
            requests.exceptions.HTTPError: If scan not found or not in
                paused state (400)
        
        Example:
            ```python
            # Resume a paused scan
            result = client.scans.resume_scan(12345)
            ```
        """
        return self._request('POST', f'scans/{scan_id}/resume')
    
    def get_all_scans(
        self,
        active: Optional[bool] = None,
        sort: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all scans with automatic pagination.
        
        Automatically handles pagination to retrieve all scans matching the
        specified criteria.
        
        Args:
            active: If True, return only running scans. If False,
                   return only completed scans. If None, return all scans.
            sort: List of sort criteria in format "property[,ASC|DESC]"
        
        Returns:
            List of all scan dictionaries
        
        Example:
            ```python
            # Get all scans
            all_scans = client.scans.get_all_scans()
            print(f"Total scans: {len(all_scans)}")
            
            # Get all active scans
            active_scans = client.scans.get_all_scans(active=True)
            ```
        """
        all_scans = []
        page = 0
        size = 500
        
        while True:
            response = self.list(active=active, page=page, size=size, sort=sort)
            scans = response.get('resources', [])
            all_scans.extend(scans)
            
            # Check if we've retrieved all pages
            page_info = response.get('page', {})
            current_page = page_info.get('number', 0)
            total_pages = page_info.get('totalPages', 1)
            
            if current_page >= total_pages - 1:
                break
            
            page += 1
        
        return all_scans
    
    def wait_for_scan_completion(
        self,
        scan_id: int,
        poll_interval: int = 30,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Wait for a scan to complete.
        
        Polls the scan status at regular intervals until the scan completes,
        is stopped, or times out.
        
        Args:
            scan_id: The unique identifier of the scan to monitor
            poll_interval: Seconds to wait between status checks
                          (default: 30)
            timeout: Maximum seconds to wait before giving up. If None,
                    waits indefinitely. (default: None)
        
        Returns:
            Final scan details dictionary
        
        Raises:
            TimeoutError: If timeout is reached before scan
                completes
            requests.exceptions.HTTPError: If scan not found
                or access denied
        
        Example:
            ```python
            # Start a scan and wait for completion
            scan_id = client.scans.start_site_scan(site_id=42)
            
            # Wait up to 2 hours
            final_scan = client.scans.wait_for_scan_completion(
                scan_id=scan_id,
                poll_interval=60,
                timeout=7200
            )
            
            print(f"Scan finished: {final_scan['status']}")
            print(f"Duration: {final_scan['duration']}")
            ```
        """
        start_time = time.time()
        
        while True:
            scan = self.get_scan(scan_id)
            status = scan.get('status', '').lower()
            
            # Check if scan is in a terminal state
            terminal_states = [
                'finished', 'stopped', 'error', 'aborted'
            ]
            if status in terminal_states:
                return scan
            
            # Check timeout
            if timeout:
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    msg = (
                        f"Scan {scan_id} did not complete within "
                        f"{timeout} seconds. Current status: {status}"
                    )
                    raise TimeoutError(msg)
            
            # Wait before next poll
            time.sleep(poll_interval)
    
    def get_scan_summary(self, scan_id: int) -> Dict[str, Any]:
        """
        Get a summary of scan results.
        
        Retrieves key metrics and status information for a scan in a
        simplified format.
        
        Args:
            scan_id: The unique identifier of the scan
        
        Returns:
            Dictionary with summary information:
                - id: Scan identifier
                - name: Scan name
                - status: Current status
                - assets_scanned: Number of assets scanned
                - vulnerabilities: Vulnerability counts by severity
                - duration: Scan duration
                - start_time: When scan started
                - end_time: When scan ended (if complete)
                - engine_name: Name of scan engine
                - message: Status message
        
        Example:
            ```python
            summary = client.scans.get_scan_summary(12345)
            print(f"Status: {summary['status']}")
            print(f"Critical: {summary['vulnerabilities']['critical']}")
            print(f"Duration: {summary['duration']}")
            ```
        """
        scan = self.get_scan(scan_id)
        
        # Extract vulnerability counts
        vulns = scan.get('vulnerabilities', {})
        
        summary = {
            'id': scan.get('id'),
            'name': scan.get('scanName'),
            'status': scan.get('status'),
            'assets_scanned': scan.get('assets', 0),
            'vulnerabilities': {
                'critical': vulns.get('critical', 0),
                'severe': vulns.get('severe', 0),
                'moderate': vulns.get('moderate', 0),
                'total': vulns.get('total', 0)
            },
            'duration': scan.get('duration'),
            'start_time': scan.get('startTime'),
            'end_time': scan.get('endTime'),
            'engine_name': scan.get('engineName'),
            'message': scan.get('message')
        }
        
        return summary
    
    def is_scan_running(self, scan_id: int) -> bool:
        """
        Check if a scan is currently running.
        
        Args:
            scan_id: The unique identifier of the scan
        
        Returns:
            True if scan is running, False otherwise
        
        Example:
            ```python
            if client.scans.is_scan_running(12345):
                print("Scan is still running")
            else:
                print("Scan has completed or stopped")
            ```
        """
        scan = self.get_scan(scan_id)
        status = scan.get('status', '').lower()
        return status == 'running'
    
    def get_active_scans(self) -> List[Dict[str, Any]]:
        """
        Get all currently running scans.
        
        Convenience method to retrieve only active scans with
        automatic pagination.
        
        Returns:
            List of active scan dictionaries
        
        Example:
            ```python
            active = client.scans.get_active_scans()
            print(f"Currently running: {len(active)} scans")
            
            for scan in active:
                print(f"- {scan['scanName']}: {scan['assets']} assets")
            ```
        """
        return self.get_all_scans(active=True)
    
    def get_completed_scans(
        self,
        sort: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all completed scans.
        
        Convenience method to retrieve only completed scans with
        automatic pagination.
        
        Args:
            sort: List of sort criteria in format "property[,ASC|DESC]"
                 Default sorts by end time descending.
        
        Returns:
            List of completed scan dictionaries
        
        Example:
            ```python
            # Get recent completed scans
            completed = client.scans.get_completed_scans(
                sort=["endTime,DESC"]
            )
            
            print(f"Last 5 completed scans:")
            for scan in completed[:5]:
                print(f"- {scan['scanName']}: {scan['endTime']}")
            ```
        """
        if sort is None:
            sort = ["endTime,DESC"]
        
        return self.get_all_scans(active=False, sort=sort)
