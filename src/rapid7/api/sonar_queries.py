"""
Sonar Query API

This module provides methods for managing InsightVM Sonar discovery queries.
"""

from typing import Dict, List, Optional, Any
from .base import BaseAPI
from ..constants import Endpoints


class SonarQueryAPI(BaseAPI):
    """API wrapper for InsightVM Sonar Query operations."""

    def __init__(
        self,
        auth,
        verify_ssl=None,
        timeout=(10, 90)
    ):
        """
        Initialize the SonarQueryAPI.

        Args:
            auth: InsightVMAuth instance
            verify_ssl: Whether to verify SSL certificates
            timeout: Tuple of (connect_timeout, read_timeout)
        """
        super().__init__(auth, verify_ssl=verify_ssl, timeout=timeout)
        self.endpoint = Endpoints.SONAR_QUERY

    def create_sonar_query(
        self,
        name: str,
        filters: List[Dict[str, Any]],
        description: Optional[str] = None
    ) -> Dict:
        """
        Create a new Sonar discovery query.

        Args:
            name: Name of the Sonar query
            filters: List of filter criteria dictionaries
            description: Optional description of the query

        Returns:
            Dict containing the created query details including ID

        Example:
            >>> filters = [
            ...     {"type": "domain-contains", "domain": "example.com"},
            ...     {"type": "scan-date-within-the-last", "days": 30}
            ... ]
            >>> result = client.sonar_queries.create_sonar_query(
            ...     name="example.com Assets",
            ...     filters=filters
            ... )
        """
        payload = {
            "name": name,
            "criteria": {"filters": filters}
        }
        
        if description:
            payload["description"] = description

        response = self.post(self.endpoint, json=payload)
        return response.json()

    def get_sonar_query(self, query_id: int) -> Dict:
        """
        Get details of a specific Sonar query.

        Args:
            query_id: ID of the Sonar query

        Returns:
            Dict containing the query details
        """
        response = self.get(f"{self.endpoint}/{query_id}")
        return response.json()

    def list_sonar_queries(
        self,
        page: int = 0,
        size: int = 10,
        sort: Optional[str] = None
    ) -> Dict:
        """
        List all Sonar queries.

        Args:
            page: Page number (0-indexed)
            size: Number of results per page
            sort: Sort order (e.g., "name,asc")

        Returns:
            Dict containing paginated list of Sonar queries
        """
        params: Dict[str, Any] = {"page": page, "size": size}
        if sort:
            params["sort"] = sort

        response = self.get(self.endpoint, params=params)
        return response.json()

    def update_sonar_query(
        self,
        query_id: int,
        name: Optional[str] = None,
        filters: Optional[List[Dict[str, Any]]] = None,
        description: Optional[str] = None
    ) -> Dict:
        """
        Update an existing Sonar query.

        Args:
            query_id: ID of the Sonar query to update
            name: New name for the query
            filters: New filter criteria
            description: New description

        Returns:
            Dict containing the updated query details
        """
        payload: Dict[str, Any] = {}
        
        if name:
            payload["name"] = name
        if filters:
            payload["criteria"] = {"filters": filters}
        if description:
            payload["description"] = description

        response = self.put(f"{self.endpoint}/{query_id}", json=payload)
        return response.json()

    def delete_sonar_query(self, query_id: int) -> None:
        """
        Delete a Sonar query.

        Args:
            query_id: ID of the Sonar query to delete
        """
        self.delete(f"{self.endpoint}/{query_id}")

    def create_domain_query(
        self,
        domain: str,
        days: int = 30,
        name: Optional[str] = None
    ) -> Dict:
        """
        Create a Sonar query for a specific domain.

        Helper method that creates a query filtering by domain and
        recent scans.

        Args:
            domain: Domain to filter by
            days: Number of days for scan recency (default: 30)
            name: Optional custom name (defaults to domain name)

        Returns:
            Dict containing the created query details

        Example:
            >>> result = sonar.create_domain_query(
            ...     domain="example.com",
            ...     days=7
            ... )
        """
        filters: List[Dict[str, Any]] = [
            {"type": "domain-contains", "domain": domain},
            {"type": "scan-date-within-the-last", "days": days}
        ]
        
        query_name = name or domain
        return self.create_sonar_query(query_name, filters)

    def create_ip_range_query(
        self,
        lower_ip: str,
        upper_ip: str,
        days: int = 30,
        name: Optional[str] = None
    ) -> Dict:
        """
        Create a Sonar query for an IP address range.

        Helper method that creates a query filtering by IP range and
        recent scans.

        Args:
            lower_ip: Lower bound IP address
            upper_ip: Upper bound IP address
            days: Number of days for scan recency (default: 30)
            name: Optional custom name (defaults to IP range)

        Returns:
            Dict containing the created query details

        Example:
            >>> result = sonar.create_ip_range_query(
            ...     lower_ip="192.168.1.1",
            ...     upper_ip="192.168.1.255",
            ...     days=7
            ... )
        """
        filters: List[Dict[str, Any]] = [
            {
                "type": "ip-address-range",
                "lower": lower_ip,
                "upper": upper_ip
            },
            {"type": "scan-date-within-the-last", "days": days}
        ]
        
        query_name = name or f"{lower_ip}-{upper_ip}"
        return self.create_sonar_query(query_name, filters)
