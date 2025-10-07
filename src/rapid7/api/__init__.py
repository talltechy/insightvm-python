"""
InsightVM API operation modules.

This package contains modules for different API operations,
all inheriting from the BaseAPI class.
"""

from .base import BaseAPI
from .scans import ScansAPI
from .reports import ReportsAPI

__all__ = ['BaseAPI', 'ScansAPI', 'ReportsAPI']
