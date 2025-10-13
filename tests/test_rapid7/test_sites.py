"""
Tests for Rapid7 InsightVM Sites API module.

Tests the sites.py API module for site management operations.
"""

import pytest
from unittest.mock import Mock, patch

from rapid7.api.sites import SiteAPI


class TestSiteAPI:
    """Test SiteAPI functionality."""

    @pytest.fixture
    def mock_auth(self):
        """Mock authentication for testing."""
        auth = Mock()
        auth.base_url = "https://test.insightvm.example.com:3780"
        auth.auth = Mock()
        return auth

    @pytest.fixture
    def sites_api(self, mock_auth):
        """Create SiteAPI instance for testing."""
        return SiteAPI(mock_auth)

    def test_init(self, mock_auth):
        """Test SiteAPI initialization."""
        api = SiteAPI(mock_auth)
        assert api.auth == mock_auth
        assert hasattr(api, 'list')
        assert hasattr(api, 'get_site')

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_list_sites(self, mock_request, sites_api):
        """Test listing all sites."""
        mock_response = {
            "resources": [
                {"id": 1, "name": "Corporate Network", "importance": "high"},
                {"id": 2, "name": "DMZ", "importance": "critical"}
            ],
            "page": {"number": 0, "size": 10}
        }
        mock_request.return_value = mock_response

        result = sites_api.list(page=0, size=10)

        assert result == mock_response
        assert len(result['resources']) == 2
        mock_request.assert_called_once()

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_get_site(self, mock_request, sites_api):
        """Test getting a specific site."""
        site_id = 123
        mock_response = {
            "id": site_id,
            "name": "Test Site",
            "importance": "high",
            "riskScore": 75000
        }
        mock_request.return_value = mock_response

        result = sites_api.get_site(site_id)

        assert result == mock_response
        assert result['id'] == site_id
        mock_request.assert_called_once_with('GET', f'sites/{site_id}')

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_create_site(self, mock_request, sites_api):
        """Test creating a new site."""
        site_config = {
            "name": "New Site",
            "description": "Test site",
            "importance": "high",
            "scanTemplate": "full-audit"
        }
        mock_response = {"id": 456}
        mock_request.return_value = mock_response

        result = sites_api.create(name="New Site", description="Test site")

        assert result == mock_response
        assert result['id'] == 456
        call_args = mock_request.call_args
        assert call_args[0][0] == 'POST'

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_update_site(self, mock_request, sites_api):
        """Test updating a site."""
        site_id = 123
        mock_response = {"id": site_id}
        mock_request.return_value = mock_response

        result = sites_api.update(site_id, name="Updated Site Name")

        assert result == mock_response
        call_args = mock_request.call_args
        assert call_args[0][0] == 'PUT'
        assert f'sites/{site_id}' in call_args[0][1]

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_delete_site(self, mock_request, sites_api):
        """Test deleting a site."""
        site_id = 123
        mock_request.return_value = {}

        result = sites_api.delete_site(site_id)

        mock_request.assert_called_once_with('DELETE', f'sites/{site_id}')

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_get_site_assets(self, mock_request, sites_api):
        """Test getting assets for a site."""
        site_id = 123
        mock_response = {
            "resources": [
                {"id": 1, "hostname": "server01.example.com"},
                {"id": 2, "hostname": "server02.example.com"}
            ]
        }
        mock_request.return_value = mock_response

        result = sites_api.get_assets(site_id)

        assert result == mock_response
        assert len(result['resources']) == 2
        call_args = mock_request.call_args
        assert f'sites/{site_id}/assets' in call_args[0][1]

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_list_with_parameters(self, mock_request, sites_api):
        """Test list with parameters."""
        mock_response = {"resources": [], "page": {}}
        mock_request.return_value = mock_response

        sites_api.list(page=0, size=100)

        mock_request.assert_called_once()
        # Just verify it was called with GET
        call_args = mock_request.call_args
        assert call_args[0][0] == 'GET'


class TestSiteAPIConfiguration:
    """Test site configuration operations."""

    @pytest.fixture
    def sites_api(self, mock_auth):
        """Create SiteAPI instance."""
        return SiteAPI(mock_auth)

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_get_scan_template(self, mock_request, sites_api):
        """Test getting site scan template."""
        site_id = 123
        mock_response = "full-audit-without-web-spider"
        mock_request.return_value = mock_response

        result = sites_api.get_scan_template(site_id)

        assert result == mock_response
        call_args = mock_request.call_args
        assert f'sites/{site_id}/scan_template' in call_args[0][1]

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_set_scan_template(self, mock_request, sites_api):
        """Test setting site scan template."""
        site_id = 123
        template_id = "full-audit"
        mock_request.return_value = {}

        result = sites_api.set_scan_template(site_id, template_id)

        call_args = mock_request.call_args
        assert call_args[0][0] == 'PUT'
        assert f'sites/{site_id}/scan_template' in call_args[0][1]

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_get_scan_engine(self, mock_request, sites_api):
        """Test getting site scan engine."""
        site_id = 123
        mock_response = {"id": 5, "name": "Engine 1"}
        mock_request.return_value = mock_response

        result = sites_api.get_scan_engine(site_id)

        assert result == mock_response
        call_args = mock_request.call_args
        assert f'sites/{site_id}/scan_engine' in call_args[0][1]

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_set_scan_engine(self, mock_request, sites_api):
        """Test setting site scan engine."""
        site_id = 123
        engine_id = 5
        mock_request.return_value = {}

        result = sites_api.set_scan_engine(site_id, engine_id)

        call_args = mock_request.call_args
        assert call_args[0][0] == 'PUT'
        assert f'sites/{site_id}/scan_engine' in call_args[0][1]


class TestSiteAPIErrorHandling:
    """Test error handling in SiteAPI."""

    @pytest.fixture
    def sites_api(self, mock_auth):
        """Create SiteAPI instance."""
        return SiteAPI(mock_auth)

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_get_nonexistent_site(self, mock_request, sites_api):
        """Test handling of 404 for nonexistent site."""
        import requests
        mock_request.side_effect = requests.HTTPError("404 Not Found")

        with pytest.raises(requests.HTTPError):
            sites_api.get_site(99999)


class TestSiteAPIIntegration:
    """Test integration scenarios."""

    @pytest.fixture
    def sites_api(self, mock_auth):
        """Create SiteAPI instance."""
        return SiteAPI(mock_auth)

    @patch('rapid7.api.sites.BaseAPI._request')
    def test_site_creation_and_configuration(self, mock_request, sites_api):
        """Test complete site workflow."""
        site_id = 456
        
        mock_request.side_effect = [
            {"id": site_id},  # create
            {},  # set_scan_template
            {},  # set_scan_engine
            {"id": site_id, "name": "New Site"}  # get
        ]

        # Create site
        created = sites_api.create({"name": "New Site"})
        assert created['id'] == site_id

        # Configure scan template
        sites_api.set_scan_template(site_id, "full-audit")

        # Configure scan engine
        sites_api.set_scan_engine(site_id, 5)

        # Verify site
        site = sites_api.get_site(site_id)
        assert site['name'] == "New Site"

        # Verify all calls were made
        assert mock_request.call_count == 4
