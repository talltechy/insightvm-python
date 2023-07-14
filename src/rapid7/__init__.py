"""
This package provides functions for interacting with the Rapid7 InsightVM API.
"""

from .api_r7_auth import (
    load_r7_platform_api_credentials,
    get_platform_api_headers,
    load_r7_isvm_api_credentials,
    get_isvm_2fa_access_token,
)

from .api_r7_isvm import (
    search_asset_isvm,
    get_asset_isvm,
    get_assets_isvm
)

__all__ = [
    "load_r7_platform_api_credentials",
    "get_platform_api_headers",
    "load_r7_isvm_api_credentials",
    "get_isvm_2fa_access_token",
    "search_asset_isvm",
    "get_asset_isvm",
    "get_assets_isvm"
]
