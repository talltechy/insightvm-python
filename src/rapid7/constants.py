"""
InsightVM API Constants

This module provides constants used throughout the InsightVM Python client,
including API endpoint paths and other configuration values.
"""

# API Version
API_VERSION = "3"
API_BASE_PATH = f"/api/{API_VERSION}"


# API Endpoints
class Endpoints:
    """API endpoint paths for InsightVM API v3."""
    
    ASSET_GROUP = "asset-group"
    ASSET = "asset"
    AUTHENTICATION = "authentication"
    CONFIGURATION = "configuration"
    CREDENTIAL = "credential"
    DISCOVERY_CONNECTION = "discovery-connection"
    DISCOVERY_PROFILE = "discovery-profile"
    ENGINE = "engine"
    EXPORT = "export"
    IMPORT = "import"
    LICENSE = "license"
    REPORT = "report"
    ROLE = "role"
    SCAN = "scan"
    SITE = "site"
    SONAR_QUERY = "sonar_queries"
    TAG = "tag"
    USER = "user"
    VULNERABILITY_EXCEPTION = "vulnerability-exception"
    VULNERABILITY = "vulnerability"
    VULNERABILITY_CHECK = "vulnerability-check"
    VULNERABILITY_DEFINITION = "vulnerability-definition"
    VULNERABILITY_SOLUTION = "vulnerability-solution"


# HTTP Status Codes
class StatusCodes:
    """Standard HTTP status codes."""
    
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


# Default Configuration
DEFAULT_TIMEOUT = 30
DEFAULT_VERIFY_SSL = False  # InsightVM often uses self-signed certs
