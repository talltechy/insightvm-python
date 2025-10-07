"""
Reports API Module for Rapid7 InsightVM

This module provides comprehensive report management functionality including:
- Report CRUD operations (list, get, create, update, delete)
- Report generation and monitoring
- Report history and instance management
- Report download and content retrieval
- Report templates and formats

Example:
    >>> from rapid7 import InsightVMClient
    >>> client = InsightVMClient()
    >>>
    >>> # List all reports
    >>> reports = client.reports.list()
    >>>
    >>> # Generate a report
    >>> instance_id = client.reports.generate(report_id=42)
    >>>
    >>> # Wait for completion and download
    >>> instance = client.reports.wait_for_completion(42, instance_id)
    >>> content = client.reports.download(42, instance_id)
"""

import time
from typing import Any, Dict, List, Optional

from .base import BaseAPI


class ReportsAPI(BaseAPI):
    """
    Handles all report-related operations for InsightVM API v3.

    This class provides methods for managing report configurations,
    generating reports, monitoring report instances, and downloading
    report content. It follows the BaseAPI inheritance pattern for
    consistent authentication and request handling.

    Attributes:
        All attributes inherited from BaseAPI including auth,
        base_url, verify_ssl, and timeout.
    """

    # Report Configuration Operations

    def list(
        self,
        page: int = 0,
        size: int = 500,
        sort: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Retrieve all report configurations.

        Args:
            page: Page number (zero-based)
            size: Number of records per page (max 500)
            sort: List of sort criteria in format
                 'property[,ASC|DESC]'

        Returns:
            Dictionary with 'resources', 'page', and 'links' keys

        Example:
            >>> reports = client.reports.list(page=0, size=100)
            >>> for report in reports['resources']:
            ...     print(f"{report['id']}: {report['name']}")
        """
        params: Dict[str, Any] = {'page': page, 'size': size}
        if sort:
            params['sort'] = sort
        return self._request('GET', 'reports', params=params)

    def get_report(self, report_id: int) -> Dict[str, Any]:
        """
        Get details of a specific report configuration.

        Args:
            report_id: The identifier of the report

        Returns:
            Dictionary containing report configuration details

        Example:
            >>> report = client.reports.get_report(42)
            >>> print(f"Report: {report['name']}")
            >>> print(f"Format: {report['format']}")
            >>> print(f"Template: {report['template']}")
        """
        return self._request('GET', f'reports/{report_id}')

    def create(self, report_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new report configuration.

        Args:
            report_config: Report configuration dictionary with keys:
                - name (str, required): Report name
                - format (str, required): Output format (pdf, html, etc.)
                - template (str): Template ID for document reports
                - scope (dict): Defines what to include (sites,
                  asset_groups, etc.)
                - filters (dict): Vulnerability filters
                - frequency (dict): Schedule configuration
                - email (dict): Email delivery settings
                - storage (dict): Storage location settings

        Returns:
            Dictionary with 'id' of created report and 'links'

        Example:
            >>> config = {
            ...     "name": "Monthly Security Report",
            ...     "format": "pdf",
            ...     "template": "executive-overview",
            ...     "scope": {
            ...         "sites": [42, 43]
            ...     }
            ... }
            >>> result = client.reports.create(config)
            >>> print(f"Created report ID: {result['id']}")
        """
        return self._request('POST', 'reports', json=report_config)

    def update(
        self,
        report_id: int,
        report_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing report configuration.

        Args:
            report_id: The identifier of the report
            report_config: Updated report configuration dictionary

        Returns:
            Dictionary with 'links' confirming update

        Example:
            >>> updated_config = {
            ...     "name": "Updated Report Name",
            ...     "format": "pdf"
            ... }
            >>> client.reports.update(42, updated_config)
        """
        return self._request('PUT', f'reports/{report_id}',
                             json=report_config)

    def delete_report(self, report_id: int) -> Dict[str, Any]:
        """
        Delete a report configuration.

        Args:
            report_id: The identifier of the report

        Returns:
            Dictionary with 'links' confirming deletion

        Example:
            >>> client.reports.delete_report(42)
        """
        return self._request('DELETE', f'reports/{report_id}')

    # Report Generation Operations

    def generate(self, report_id: int) -> int:
        """
        Generate a report and return the instance ID.

        Args:
            report_id: The identifier of the report to generate

        Returns:
            Integer instance ID of the generated report

        Example:
            >>> instance_id = client.reports.generate(42)
            >>> print(f"Report generation started: {instance_id}")
        """
        result = self._request('POST', f'reports/{report_id}/generate')
        return result['id']

    # Report History and Instance Operations

    def get_history(self, report_id: int) -> Dict[str, Any]:
        """
        Get all historical instances of a report.

        Args:
            report_id: The identifier of the report

        Returns:
            Dictionary with list of report instances in 'resources'

        Example:
            >>> history = client.reports.get_history(42)
            >>> for instance in history['resources']:
            ...     print(f"Instance {instance['id']}: "
            ...           f"{instance['status']}")
        """
        return self._request('GET', f'reports/{report_id}/history')

    def get_instance(
        self,
        report_id: int,
        instance_id: str
    ) -> Dict[str, Any]:
        """
        Get details of a specific report instance.

        Args:
            report_id: The identifier of the report
            instance_id: The identifier of the report instance

        Returns:
            Dictionary with instance details including status, size,
            generated time, and download URI

        Example:
            >>> instance = client.reports.get_instance(42, "12345")
            >>> print(f"Status: {instance['status']}")
            >>> print(f"Size: {instance['size']['formatted']}")
            >>> print(f"Generated: {instance['generated']}")
        """
        return self._request(
            'GET',
            f'reports/{report_id}/history/{instance_id}'
        )

    def delete_instance(
        self,
        report_id: int,
        instance_id: str
    ) -> Dict[str, Any]:
        """
        Delete a specific report instance.

        Args:
            report_id: The identifier of the report
            instance_id: The identifier of the report instance

        Returns:
            Dictionary with 'links' confirming deletion

        Example:
            >>> client.reports.delete_instance(42, "12345")
        """
        return self._request(
            'DELETE',
            f'reports/{report_id}/history/{instance_id}'
        )

    def download(
        self,
        report_id: int,
        instance_id: str
    ) -> bytes:
        """
        Download the content of a generated report.

        The content is typically returned in GZip compressed format.

        Args:
            report_id: The identifier of the report
            instance_id: The identifier of the report instance

        Returns:
            Bytes content of the report (usually GZip compressed)

        Example:
            >>> content = client.reports.download(42, "12345")
            >>> with open("report.pdf.gz", "wb") as f:
            ...     f.write(content)
        """
        response = self._request(
            'GET',
            f'reports/{report_id}/history/{instance_id}/output',
            return_raw=True
        )
        return response.content

    # Template and Format Operations

    def get_templates(self) -> Dict[str, Any]:
        """
        Get all available report templates.

        Returns:
            Dictionary with list of templates in 'resources'

        Example:
            >>> templates = client.reports.get_templates()
            >>> for template in templates['resources']:
            ...     print(f"{template['id']}: {template['name']}")
            ...     print(f"  Type: {template['type']}")
            ...     print(f"  Built-in: {template['builtin']}")
        """
        return self._request('GET', 'report_templates')

    def get_template(self, template_id: str) -> Dict[str, Any]:
        """
        Get details of a specific report template.

        Args:
            template_id: The identifier of the template

        Returns:
            Dictionary with template details

        Example:
            >>> template = client.reports.get_template(
            ...     "executive-overview"
            ... )
            >>> print(f"Name: {template['name']}")
            >>> print(f"Description: {template['description']}")
        """
        return self._request('GET', f'report_templates/{template_id}')

    def get_formats(self) -> Dict[str, Any]:
        """
        Get all available report formats.

        Returns:
            Dictionary with list of formats in 'resources'

        Example:
            >>> formats = client.reports.get_formats()
            >>> for fmt in formats['resources']:
            ...     print(f"Format: {fmt['format']}")
            ...     if 'templates' in fmt:
            ...         print(f"  Templates: {fmt['templates']}")
        """
        return self._request('GET', 'report_formats')

    # Helper Methods

    def wait_for_completion(
        self,
        report_id: int,
        instance_id: str,
        poll_interval: int = 30,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Wait for a report generation to complete.

        Polls the report instance status until it's complete or
        the timeout is reached.

        Args:
            report_id: The identifier of the report
            instance_id: The identifier of the report instance
            poll_interval: Seconds between status checks (default: 30)
            timeout: Maximum seconds to wait (None = wait indefinitely)

        Returns:
            Final report instance details dictionary

        Raises:
            TimeoutError: If timeout is reached before completion

        Example:
            >>> instance_id = client.reports.generate(42)
            >>> instance = client.reports.wait_for_completion(
            ...     42,
            ...     instance_id,
            ...     poll_interval=60,
            ...     timeout=3600
            ... )
            >>> print(f"Report complete: {instance['status']}")
        """
        start_time = time.time()
        while True:
            instance = self.get_instance(report_id, instance_id)
            status = instance.get('status', '').lower()

            if status == 'complete':
                return instance
            elif status in ['failed', 'aborted', 'unknown']:
                raise RuntimeError(
                    f"Report generation {status}: {instance}"
                )

            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                raise TimeoutError(
                    f"Report generation timed out after {timeout} seconds"
                )

            time.sleep(poll_interval)

    def is_complete(self, report_id: int, instance_id: str) -> bool:
        """
        Check if a report generation is complete.

        Args:
            report_id: The identifier of the report
            instance_id: The identifier of the report instance

        Returns:
            True if report is complete, False otherwise

        Example:
            >>> if client.reports.is_complete(42, "12345"):
            ...     content = client.reports.download(42, "12345")
        """
        instance = self.get_instance(report_id, instance_id)
        return instance.get('status', '').lower() == 'complete'

    def get_latest_instance(self, report_id: int) -> Optional[Dict[str, Any]]:
        """
        Get the most recent report instance.

        Args:
            report_id: The identifier of the report

        Returns:
            Dictionary with latest instance details, or None if no history

        Example:
            >>> latest = client.reports.get_latest_instance(42)
            >>> if latest:
            ...     print(f"Latest: {latest['generated']}")
        """
        history = self.get_history(report_id)
        instances = history.get('resources', [])
        if not instances:
            return None
        # Sort by generation time, most recent first
        sorted_instances = sorted(
            instances,
            key=lambda x: x.get('generated', ''),
            reverse=True
        )
        return sorted_instances[0] if sorted_instances else None

    def get_all_reports(
        self,
        sort: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all report configurations across all pages.

        Args:
            sort: List of sort criteria

        Returns:
            List of all report configuration dictionaries

        Example:
            >>> all_reports = client.reports.get_all_reports()
            >>> print(f"Total reports: {len(all_reports)}")
        """
        all_reports = []
        page = 0
        while True:
            response = self.list(page=page, size=500, sort=sort)
            resources = response.get('resources', [])
            if not resources:
                break
            all_reports.extend(resources)
            page_info = response.get('page', {})
            if page >= page_info.get('totalPages', 0) - 1:
                break
            page += 1
        return all_reports

    def generate_and_download(
        self,
        report_id: int,
        poll_interval: int = 30,
        timeout: Optional[int] = 3600
    ) -> bytes:
        """
        Generate a report, wait for completion, and download content.

        This is a convenience method that combines generate,
        wait_for_completion, and download into a single operation.

        Args:
            report_id: The identifier of the report
            poll_interval: Seconds between status checks (default: 30)
            timeout: Maximum seconds to wait (default: 3600)

        Returns:
            Bytes content of the generated report

        Example:
            >>> content = client.reports.generate_and_download(
            ...     42,
            ...     poll_interval=60
            ... )
            >>> with open("report.pdf.gz", "wb") as f:
            ...     f.write(content)
        """
        instance_id = str(self.generate(report_id))
        self.wait_for_completion(
            report_id,
            instance_id,
            poll_interval=poll_interval,
            timeout=timeout
        )
        return self.download(report_id, instance_id)
