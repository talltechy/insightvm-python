"""
Tests for Rapid7 InsightVM BaseAPI class.

Tests the foundational API functionality that all other API modules inherit from,
including request handling, SSL configuration, and error management.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

from rapid7.api.base import BaseAPI
from rapid7.auth import InsightVMAuth


class TestBaseAPI:
    """Test BaseAPI core functionality."""

    @pytest.fixture
    def mock_auth(self):
        """Mock authentication object for testing."""
        auth = Mock()
        auth.base_url = "https://test.insightvm.example.com:3780"
        auth.auth = Mock()  # HTTPBasicAuth mock
        return auth

    @pytest.fixture
    def api_client(self, mock_auth):
        """Create BaseAPI client for testing."""
        return BaseAPI(mock_auth)

    def test_init_basic(self, mock_auth):
        """Test basic BaseAPI initialization."""
        api = BaseAPI(mock_auth)
        assert api.auth == mock_auth
        assert api.base_url == "https://test.insightvm.example.com:3780"
        assert api.timeout == (10, 90)
        assert api.verify_ssl == True  # Default from env var in conftest

    def test_init_ssl_verification_disabled(self, mock_auth):
        """Test SSL verification can be disabled."""
        api = BaseAPI(mock_auth, verify_ssl=False)
        assert api.verify_ssl == False

    def test_init_custom_timeout(self, mock_auth):
        """Test custom timeout configuration."""
        custom_timeout = (5, 120)
        api = BaseAPI(mock_auth, timeout=custom_timeout)
        assert api.timeout == custom_timeout

    def test_build_url_simple(self, api_client):
        """Test simple URL building."""
        url = api_client._build_url("assets")
        expected = "https://test.insightvm.example.com:3780/api/3/assets"
        assert url == expected

    def test_build_url_with_leading_slash(self, api_client):
        """Test URL building handles leading slashes."""
        url = api_client._build_url("/assets")
        expected = "https://test.insightvm.example.com:3780/api/3/assets"
        assert url == expected

    def test_build_url_complex_endpoint(self, api_client):
        """Test URL building for complex endpoints."""
        url = api_client._build_url("assets/123/vulnerabilities")
        expected = "https://test.insightvm.example.com:3780/api/3/assets/123/vulnerabilities"
        assert url == expected

    @patch('rapid7.api.base.requests.request')
    def test_request_success_json_response(self, mock_request, api_client, mock_api_response):
        """Test successful JSON request returns parsed data."""
        mock_request.return_value = mock_api_response

        result = api_client._request('GET', 'test/endpoint')

        assert result == {"status": "success", "data": []}
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[0][0] == 'GET'  # method
        assert 'https://test.insightvm.example.com:3780/api/3/test/endpoint' in call_args[0][1]  # url

    @patch('rapid7.api.base.requests.request')
    def test_request_success_raw_response(self, mock_request, api_client, mock_api_response):
        """Test return_raw=True returns raw Response object."""
        mock_request.return_value = mock_api_response

        result = api_client._request('GET', 'test/endpoint', return_raw=True)

        assert result is mock_api_response  # Should return raw response
        mock_request.assert_called_once()

    @patch('rapid7.api.base.requests.request')
    def test_request_with_params(self, mock_request, api_client, mock_api_response):
        """Test request includes query parameters."""
        mock_request.return_value = mock_api_response

        params = {"page": 0, "size": 100}
        api_client._request('GET', 'assets', params=params)

        call_args = mock_request.call_args
        assert call_args[1]['params'] == params

    @patch('rapid7.api.base.requests.request')
    def test_request_with_json_body(self, mock_request, api_client, mock_api_response):
        """Test request includes JSON body data."""
        mock_request.return_value = mock_api_response

        json_data = {"name": "test-group"}
        api_client._request('POST', 'asset_groups', json=json_data)

        call_args = mock_request.call_args
        assert call_args[1]['json'] == json_data

    @patch('rapid7.api.base.requests.request')
    def test_request_with_headers(self, mock_request, api_client, mock_api_response):
        """Test request includes custom headers."""
        mock_request.return_value = mock_api_response

        custom_headers = {"X-Custom": "test"}
        api_client._request('GET', 'assets', headers=custom_headers)

        call_args = mock_request.call_args
        assert call_args[1]['headers'] == custom_headers

    @patch('rapid7.api.base.requests.request')
    def test_request_default_auth_and_verify(self, mock_request, api_client, mock_api_response):
        """Test request applies default auth and SSL verification."""
        mock_request.return_value = mock_api_response

        api_client._request('GET', 'test')

        call_args = mock_request.call_args
        assert call_args[1]['auth'] == api_client.auth.auth
        assert call_args[1]['verify'] == api_client.verify_ssl
        assert call_args[1]['timeout'] == api_client.timeout

    @patch('rapid7.api.base.requests.request')
    def test_request_timeout_override(self, mock_request, api_client, mock_api_response):
        """Test timeout can be overridden per request."""
        mock_request.return_value = mock_api_response

        custom_timeout = (30, 300)
        api_client._request('GET', 'test', timeout=custom_timeout)

        call_args = mock_request.call_args
        assert call_args[1]['timeout'] == custom_timeout

    @patch('rapid7.api.base.requests.request')
    def test_request_http_error_handling(self, mock_request, api_client):
        """Test HTTP error handling."""
        # Create an error response
        error_response = Mock()
        error_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_request.return_value = error_response

        with pytest.raises(requests.HTTPError):
            api_client._request('GET', 'nonexistent')

    @patch('rapid7.api.base.requests.request')
    def test_request_network_error_handling(self, mock_request, api_client):
        """Test network error handling."""
        mock_request.side_effect = requests.ConnectionError("Network error")

        with pytest.raises(requests.ConnectionError):
            api_client._request('GET', 'test')

    def test_legacy_get_method(self, api_client, mock_api_response):
        """Test legacy get() method returns raw Response."""
        with patch('rapid7.api.base.requests.request') as mock_request:
            mock_request.return_value = mock_api_response

            result = api_client.get('assets')
            assert result is mock_api_response

            # Verify it calls _request with return_raw=True internally
            mock_request.assert_called_once()

    def test_legacy_post_method(self, api_client, mock_api_response):
        """Test legacy post() method returns raw Response."""
        with patch('rapid7.api.base.requests.request') as mock_request:
            mock_request.return_value = mock_api_response

            json_data = {"test": "data"}
            result = api_client.post('assets', json=json_data)
            assert result is mock_api_response

            call_args = mock_request.call_args
            assert call_args[1]['json'] == json_data

    def test_legacy_put_method(self, api_client, mock_api_response):
        """Test legacy put() method returns raw Response."""
        with patch('rapid7.api.base.requests.request') as mock_request:
            mock_request.return_value = mock_api_response

            json_data = {"test": "data"}
            result = api_client.put('assets/123', json=json_data)
            assert result is mock_api_response

    def test_legacy_delete_method(self, api_client, mock_api_response):
        """Test legacy delete() method returns raw Response."""
        with patch('rapid7.api.base.requests.request') as mock_request:
            mock_request.return_value = mock_api_response

            result = api_client.delete('assets/123')
            assert result is mock_api_response

    def test_ssl_warning_suppression(self, mock_auth):
        """Test SSL warnings are suppressed when verification is disabled."""
        with patch('urllib3.disable_warnings') as mock_disable_warnings:
            api = BaseAPI(mock_auth, verify_ssl=False)
            # disable_warnings should be called once during init
            mock_disable_warnings.assert_called_once()


class TestBaseAPIIntegration:
    """Test BaseAPI in more complex scenarios."""

    def test_multiple_requests_different_methods(self, api_client):
        """Test multiple requests with different HTTP methods."""
        methods_and_endpoints = [
            ('GET', 'assets'),
            ('POST', 'asset_groups'),
            ('PUT', 'sites/123'),
            ('DELETE', 'assets/456')
        ]

        with patch('rapid7.api.base.requests.request') as mock_request:
            mock_response = Mock()
            mock_response.json.return_value = {"status": "success"}
            mock_request.return_value = mock_response

            for method, endpoint in methods_and_endpoints:
                result = api_client._request(method, endpoint)
                assert result["status"] == "success"

            # Should have made 4 separate calls
            assert mock_request.call_count == 4

    def test_json_parsing_edge_cases(self, api_client):
        """Test JSON parsing with various response structures."""
        test_cases = [
            ({"data": [], "meta": {}}, "empty data"),
            ({"resources": [{"id": 1}], "page": {"total": 1}}, "paginated list"),
            ({"id": 123, "name": "test"}, "single resource"),
            ([], "empty array response"),
        ]

        with patch('rapid7.api.base.requests.request') as mock_request:
            for expected_data, description in test_cases:
                mock_response = Mock()
                mock_response.json.return_value = expected_data
                mock_request.return_value = mock_response

                result = api_client._request('GET', 'test')
                assert result == expected_data

    def test_binary_content_handling(self, api_client):
        """Test binary content handling doesn't attempt JSON parsing."""
        with patch('rapid7.api.base.requests.request') as mock_request:
            binary_response = Mock()
            binary_response.content = b"binary content here"
            # Binary response might not be valid JSON
            binary_response.json.side_effect = ValueError("Not JSON")
            mock_request.return_value = binary_response

            result = api_client._request('GET', 'reports/1/download', return_raw=True)
            assert result is binary_response  # Should return raw response
            # Should not call json() method for raw responses
            binary_response.json.assert_not_called()
