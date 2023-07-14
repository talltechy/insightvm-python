"""
This module provides functions for authenticating and working with the Palo Alto Cortex XDR API.

Functions:
- load_xdr_api_credentials: loads the XDR API credentials from a configuration file
- generate_advanced_authentication: generates an advanced authentication token for the XDR API
- unisolate_endpoint: unisolates an endpoint in the XDR API
- get_endpoint_quarantine_status: gets the quarantine status of an endpoint in the XDR API
- quarantine_endpoint: quarantines an endpoint in the XDR API
- unquarantine_endpoint: unquarantines an endpoint in the XDR API
- get_endpoint_network_details: gets the network details of an endpoint in the XDR API
"""

from .api_pa_xdr_auth import (
    load_xdr_api_credentials,
    generate_advanced_authentication
)

from .api_pa_xdr import (
    unisolate_endpoint,
    get_endpoint_quarantine_status,
    quarantine_endpoint,
    unquarantine_endpoint,
    get_endpoint_network_details,
)

__all__ = [
    "load_xdr_api_credentials",
    "generate_advanced_authentication",
    "unisolate_endpoint",
    "get_endpoint_quarantine_status",
    "quarantine_endpoint",
    "unquarantine_endpoint",
    "get_endpoint_network_details",
    "api_pa_xdr"
]
