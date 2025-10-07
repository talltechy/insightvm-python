"""
Rapid7 InsightVM Python Client

A modern, simplified Python client for Rapid7 InsightVM API.

Usage:
    >>> from src.rapid7 import InsightVMClient
    >>> 
    >>> # Create client (uses environment variables)
    >>> client = InsightVMClient()
    >>> 
    >>> # List assets
    >>> assets = client.assets.list()
    >>> 
    >>> # Create asset group
    >>> group = client.asset_groups.create_high_risk()

Environment Variables:
    INSIGHTVM_API_USERNAME: Your InsightVM username
    INSIGHTVM_API_PASSWORD: Your InsightVM password
    INSIGHTVM_BASE_URL: Your InsightVM instance URL
    INSIGHTVM_VERIFY_SSL: Whether to verify SSL (default: true)
"""

from .client import InsightVMClient, create_client
from .auth import InsightVMAuth, PlatformAuth

__version__ = '2.0.0'
__all__ = [
    'InsightVMClient',
    'create_client',
    'InsightVMAuth',
    'PlatformAuth',
]
