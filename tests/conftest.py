"""
Shared test fixtures and utilities for InsightVM-Python tests.

This module provides common test fixtures, mocks, and utilities used
across the test suite.
"""
import os
import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

# Mock environment variables for testing
MOCK_ENV_VARS = {
    "INSIGHTVM_API_USERNAME": "test_user",
    "INSIGHTVM_API_PASSWORD": "test_pass",
    "INSIGHTVM_BASE_URL": "https://test.insightvm.example.com:3780",
    "INSIGHTVM_VERIFY_SSL": "true",
    "INSIGHT_PLATFORM_API_KEY": "test_platform_key",
    "INSIGHT_PLATFORM_BASE_URL": "https://us.api.insight.rapid7.com",
    "XDR_API_KEY": "test_xdr_key",
    "XDR_API_KEY_ID": "test_xdr_key_id",
    "XDR_BASE_URL": "https://api-test.xdr.us.paloaltonetworks.com",
}


@pytest.fixture(autouse=True)
def mock_environment_variables():
    """
    Automatically mock all environment variables for all tests.

    This ensures tests don't depend on real credentials and run consistently
    across environments.
    """
    with patch.dict(os.environ, MOCK_ENV_VARS):
        yield


@pytest.fixture
def mock_requests_session():
    """
    Mock requests.Session for testing HTTP interactions.

    Provides a mock that captures all HTTP calls without making real requests.
    """
    with patch('requests.Session') as mock_session:
        mock_instance = Mock()
        mock_session.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_api_response():
    """
    Mock API response object for testing.

    Returns a Mock object that behaves like a requests.Response.
    """
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"status": "success", "data": []}
    response.headers = {"Content-Type": "application/json"}
    return response


@pytest.fixture
def mock_auth_headers():
    """
    Mock authentication headers for Platform API.

    Returns typical headers for Insight Platform API requests.
    """
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Key": "test_platform_key",
    }


@pytest.fixture
def mock_asset_data():
    """
    Mock asset data for testing asset-related operations.

    Returns realistic mock asset data that matches InsightVM API structure.
    """
    return {
        "id": 12345,
        "hostname": "test-server.example.com",
        "ip": "192.168.1.100",
        "mac": "00:11:22:33:44:55",
        "os": "Linux",
        "addresses": ["192.168.1.100"],
        "type": "computer",
        "criticality": "high",
        "groups": [],
        "links": [
            {"href": "https://api.example.com/assets/12345", "rel": "self"}
        ],
        "riskScore": 85.5,
        "vulnerabilities": {
            "total": 10,
            "critical": 2,
            "high": 3,
            "medium": 3,
            "low": 2,
        },
    }


@pytest.fixture
def mock_assets_list():
    """
    Mock list of assets for testing bulk operations.

    Returns a realistic response structure for asset listing endpoints.
    """
    return {
        "resources": [
            {
                "id": 12345,
                "hostname": "test-server-01.example.com",
                "ip": "192.168.1.100",
            },
            {
                "id": 12346,
                "hostname": "test-server-02.example.com",
                "ip": "192.168.1.101",
            },
            {
                "id": 12347,
                "hostname": "test-server-03.example.com",
                "ip": "192.168.1.102",
            },
        ],
        "page": {
            "number": 0,
            "size": 10,
            "totalResources": 3,
            "totalPages": 1,
        },
    }


@pytest.fixture
def mock_paginated_response():
    """
    Mock paginated API response.

    Returns a response structure that includes pagination metadata.
    """
    return {
        "resources": [mock_asset_data()],
        "page": {
            "number": 0,
            "size": 10,
            "totalResources": 150,
            "totalPages": 15,
        },
        "links": [
            {"href": "?page=0&size=10", "rel": "first"},
            {"href": "?page=1&size=10", "rel": "next"},
            {"href": "?page=14&size=10", "rel": "last"},
        ],
    }


# Utility functions for tests
def assert_api_call(mock_session, method: str, expected_url: str, headers=None):
    """
    Assert that an API call was made correctly.

    Utility function to verify HTTP calls in tests.
    """
    # Find the specific call
    calls = [call for call in mock_session.request.call_args_list
             if call[0][0] == method and expected_url in call[0][1]]

    assert len(calls) > 0, f"No {method} call to {expected_url} found"

    if headers:
        call_args = calls[-1]  # Get the last call (most recent)
        call_headers = call_args[1].get('headers', {})
        for key, value in headers.items():
            assert call_headers.get(key) == value, f"Header {key} != {value}"


def create_mock_response(data: Dict[str, Any], status_code: int = 200) -> Mock:
    """
    Create a mock requests.Response object with given data.

    Utility for creating consistent mock responses in tests.
    """
    response = Mock()
    response.status_code = status_code
    response.json.return_value = data
    response.headers = {"Content-Type": "application/json"}
    response.content = b"mock content" if status_code >= 400 else data
    return response


# Custom pytest marks
pytestmark = [
    pytest.mark.unit,
]
