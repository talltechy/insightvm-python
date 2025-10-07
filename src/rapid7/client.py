"""
Unified InsightVM Client.

This module provides the main client interface for interacting with
Rapid7 InsightVM API, consolidating all operations into a single,
easy-to-use client.
"""

from typing import Optional, Tuple
from .auth import InsightVMAuth
from .api.assets import AssetAPI
from .api.asset_groups import AssetGroupAPI
from .api.sites import SiteAPI
from .api.sonar_queries import SonarQueryAPI
from .api.scans import ScansAPI
from .api.reports import ReportsAPI


class InsightVMClient:
    """
    Main client for interacting with Rapid7 InsightVM API.
    
    This client provides a unified interface to all InsightVM operations
    through organized sub-clients for different resource types.
    
    Attributes:
        auth (InsightVMAuth): Authentication handler
        assets (AssetAPI): Asset operations client
        asset_groups (AssetGroupAPI): Asset group operations client
        sonar_queries (SonarQueryAPI): Sonar query operations client
        sites (SiteAPI): Site operations client
        scans (ScansAPI): Scan operations client
        reports (ReportsAPI): Report operations client
    
    Example:
        >>> # Basic usage with environment variables
        >>> client = InsightVMClient()
        >>> 
        >>> # List all assets
        >>> assets = client.assets.list(page=0, size=100)
        >>> 
        >>> # Create high-risk asset group
        >>> group = client.asset_groups.create_high_risk()
        >>> 
        >>> # Search for assets
        >>> results = client.assets.search({
        ...     'filters': [{
        ...         'field': 'risk-score',
        ...         'operator': 'is-greater-than',
        ...         'value': 5000
        ...     }],
        ...     'match': 'all'
        ... })
        >>> 
        >>> # With explicit credentials
        >>> client = InsightVMClient(
        ...     username="admin",
        ...     password="password",
        ...     base_url="https://insightvm.example.com",
        ...     verify_ssl=False
        ... )
    """
    
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        timeout: Tuple[int, int] = (10, 90)
    ):
        """
        Initialize the InsightVM client.
        
        Args:
            username: InsightVM API username (optional, from env
                     if not provided)
            password: InsightVM API password (optional, from env
                     if not provided)
            base_url: InsightVM base URL (optional, from env
                     if not provided)
            verify_ssl: Whether to verify SSL certificates
                       (default: from env or True)
            timeout: Tuple of (connect_timeout, read_timeout) in seconds
        
        Raises:
            ValueError: If required credentials are missing
        
        Example:
            >>> # Use environment variables
            >>> client = InsightVMClient()
            >>> 
            >>> # Or provide credentials explicitly
            >>> client = InsightVMClient(
            ...     username="admin",
            ...     password="password",
            ...     base_url="https://insightvm.example.com"
            ... )
        """
        # Initialize authentication
        self.auth = InsightVMAuth(
            username=username,
            password=password,
            base_url=base_url
        )
        
        # Initialize API clients
        self.assets = AssetAPI(
            self.auth, verify_ssl=verify_ssl, timeout=timeout
        )
        self.asset_groups = AssetGroupAPI(
            self.auth, verify_ssl=verify_ssl, timeout=timeout
        )
        self.sonar_queries = SonarQueryAPI(
            self.auth, verify_ssl=verify_ssl, timeout=timeout
        )
        self.sites = SiteAPI(
            self.auth, verify_ssl=verify_ssl, timeout=timeout
        )
        self.scans = ScansAPI(
            self.auth, verify_ssl=verify_ssl, timeout=timeout
        )
        self.reports = ReportsAPI(
            self.auth, verify_ssl=verify_ssl, timeout=timeout
        )
    
    def __repr__(self):
        return f"InsightVMClient(base_url='{self.auth.base_url}')"
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        # Can add cleanup logic here if needed in the future
        pass


# Convenience function for quick client creation
def create_client(
    username: Optional[str] = None,
    password: Optional[str] = None,
    base_url: Optional[str] = None,
    **kwargs
) -> InsightVMClient:
    """
    Create an InsightVM client with simplified interface.
    
    This is a convenience function that creates and returns
    an InsightVMClient instance.
    
    Args:
        username: InsightVM API username
        password: InsightVM API password
        base_url: InsightVM base URL
        **kwargs: Additional arguments passed to InsightVMClient
    
    Returns:
        Configured InsightVMClient instance
    
    Example:
        >>> from src.rapid7.client import create_client
        >>> 
        >>> client = create_client()
        >>> assets = client.assets.list()
    """
    return InsightVMClient(
        username=username,
        password=password,
        base_url=base_url,
        **kwargs
    )
