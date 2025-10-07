"""
InsightVM API operation modules.

This package contains modules for different API operations,
all inheriting from the BaseAPI class.
"""

from .base import BaseAPI
from .scans import ScansAPI

__all__ = ['BaseAPI', 'ScansAPI']
