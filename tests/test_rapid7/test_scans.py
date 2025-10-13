"""
Tests for Rapid7 InsightVM Scans API module.

Tests the scans.py API module for scan lifecycle management.
"""

import pytest
from unittest.mock import Mock, patch

from rapid7.api.scans import ScansAPI


class TestScansAPI:
    """Test ScansAPI functionality."""

    @pytest.fixture
    def mock_auth(self):
        """Mock authentication for testing."""
        auth = Mock()
        auth.base_url = "https://test.insightvm.example.com:3780"
        auth.auth = Mock()
        return auth

    @pytest.fixture
    def scans_api(self, mock_auth):
        """Create ScansAPI instance for testing."""
        return ScansAPI(mock_auth)

    def test_init(self, mock_auth):
        """Test ScansAPI initialization."""
        api = ScansAPI(mock_auth)
        assert api.auth == mock_auth
        assert hasattr(api, 'MAX_PAGE_SIZE')
        assert api.MAX_PAGE_SIZE == 500

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_list_scans(self, mock_request, scans_api):
        """Test listing all scans."""
        mock_response = {
            "resources": [
                {"id": 1, "scanName": "Test Scan 1", "status": "running"},
                {"id": 2, "scanName": "Test Scan 2", "status": "finished"}
            ],
            "page": {"number": 0, "size": 10, "totalResources": 2}
        }
        mock_request.return_value = mock_response

        result = scans_api.list(page=0, size=10)

        assert result == mock_response
        assert len(result['resources']) == 2
        mock_request.assert_called_once()

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_list_active_scans(self, mock_request, scans_api):
        """Test listing only active scans."""
        mock_response = {
            "resources": [{"id": 1, "status": "running"}],
            "page": {"number": 0, "size": 10}
        }
        mock_request.return_value = mock_response

        result = scans_api.list(active=True)

        assert result == mock_response
        mock_request.assert_called_once()
        # Verify active parameter was passed (as string 'true')
        call_args = mock_request.call_args
        assert call_args[1]['params']['active'] == 'true'

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_get_scan(self, mock_request, scans_api):
        """Test getting a specific scan."""
        scan_id = 123
        mock_response = {
            "id": scan_id,
            "scanName": "Security Audit",
            "status": "running",
            "progress": 45.5
        }
        mock_request.return_value = mock_response

        result = scans_api.get_scan(scan_id)

        assert result == mock_response
        assert result['id'] == scan_id
        mock_request.assert_called_once_with('GET', f'scans/{scan_id}')

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_start_site_scan(self, mock_request, scans_api):
        """Test starting a scan for a site."""
        site_id = 456
        mock_response = {"id": 789}  # API returns dict with id
        mock_request.return_value = mock_response

        result = scans_api.start_site_scan(
            site_id=site_id,
            scan_name="Test Scan",
            scan_template_id="full-audit"
        )

        assert result == 789  # Method extracts the ID
        mock_request.assert_called_once()
        # Verify it's a POST request to the correct endpoint
        call_args = mock_request.call_args
        assert call_args[0][0] == 'POST'
        assert f'sites/{site_id}/scans' in call_args[0][1]

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_start_site_scan_with_hosts(self, mock_request, scans_api):
        """Test starting a scan with specific hosts."""
        site_id = 456
        hosts = ["192.168.1.100", "192.168.1.101"]
        mock_response = {"id": 789}  # API returns dict with id
        mock_request.return_value = mock_response

        result = scans_api.start_site_scan(
            site_id=site_id,
            hosts=hosts
        )

        assert result == 789  # Method extracts the ID
        call_args = mock_request.call_args
        assert 'hosts' in call_args[1]['json']
        assert call_args[1]['json']['hosts'] == hosts

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_stop_scan(self, mock_request, scans_api):
        """Test stopping a running scan."""
        scan_id = 123
        mock_request.return_value = {}

        result = scans_api.stop_scan(scan_id)

        mock_request.assert_called_once_with('POST', f'scans/{scan_id}/stop')

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_pause_scan(self, mock_request, scans_api):
        """Test pausing a running scan."""
        scan_id = 123
        mock_request.return_value = {}

        result = scans_api.pause_scan(scan_id)

        mock_request.assert_called_once_with('POST', f'scans/{scan_id}/pause')

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_resume_scan(self, mock_request, scans_api):
        """Test resuming a paused scan."""
        scan_id = 123
        mock_request.return_value = {}

        result = scans_api.resume_scan(scan_id)

        mock_request.assert_called_once_with('POST', f'scans/{scan_id}/resume')

    @patch('rapid7.api.scans.ScansAPI.get_scan')
    def test_get_scan_summary(self, mock_get_scan, scans_api):
        """Test getting scan summary."""
        scan_id = 123
        mock_full_scan = {
            "id": scan_id,
            "scanName": "Test Scan",
            "status": "running",
            "assets": 50,
            "vulnerabilities": {
                "critical": 5,
                "severe": 10,
                "moderate": 20,
                "total": 35
            },
            "duration": "00:30:00"
        }
        mock_get_scan.return_value = mock_full_scan

        result = scans_api.get_scan_summary(scan_id)

        assert result['status'] == "running"
        assert result['assets_scanned'] == 50
        assert result['vulnerabilities']['critical'] == 5

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_list_with_pagination(self, mock_request, scans_api):
        """Test list respects page size limits."""
        mock_response = {"resources": [], "page": {}}
        mock_request.return_value = mock_response

        # Request larger than MAX_PAGE_SIZE
        scans_api.list(page=0, size=1000)

        call_args = mock_request.call_args
        # Should be capped at MAX_PAGE_SIZE (500)
        assert call_args[1]['params']['size'] == 500

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_list_with_sort(self, mock_request, scans_api):
        """Test list with sort parameters."""
        mock_response = {"resources": [], "page": {}}
        mock_request.return_value = mock_response

        sort_params = ["startTime,DESC", "scanName,ASC"]
        scans_api.list(sort=sort_params)

        call_args = mock_request.call_args
        assert call_args[1]['params']['sort'] == sort_params


class TestScansAPIUtilityMethods:
    """Test utility methods."""

    @pytest.fixture
    def scans_api(self, mock_auth):
        """Create ScansAPI instance."""
        return ScansAPI(mock_auth)

    @patch('rapid7.api.scans.ScansAPI.list')
    def test_get_active_scans(self, mock_list, scans_api):
        """Test getting active scans."""
        mock_response = [
            {"id": 1, "status": "running"},
            {"id": 2, "status": "running"}
        ]
        mock_list.return_value = {"resources": mock_response}

        result = scans_api.get_active_scans()

        assert len(result) == 2
        assert all(scan['status'] == 'running' for scan in result)


class TestScansAPIScanHistory:
    """Test scan history operations."""

    @pytest.fixture
    def scans_api(self, mock_auth):
        """Create ScansAPI instance."""
        return ScansAPI(mock_auth)

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_get_site_scans(self, mock_request, scans_api):
        """Test getting scans for a specific site."""
        site_id = 123
        mock_response = {
            "resources": [
                {"id": 1, "scanName": "Scan 1"},
                {"id": 2, "scanName": "Scan 2"}
            ]
        }
        mock_request.return_value = mock_response

        result = scans_api.get_site_scans(site_id)

        assert result == mock_response
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert f'sites/{site_id}/scans' in call_args[0][1]


class TestScansAPIErrorHandling:
    """Test error handling in ScansAPI."""

    @pytest.fixture
    def scans_api(self, mock_auth):
        """Create ScansAPI instance."""
        return ScansAPI(mock_auth)

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_get_nonexistent_scan(self, mock_request, scans_api):
        """Test handling of 404 for nonexistent scan."""
        import requests
        mock_request.side_effect = requests.HTTPError("404 Not Found")

        with pytest.raises(requests.HTTPError):
            scans_api.get_scan(99999)

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_stop_already_stopped_scan(self, mock_request, scans_api):
        """Test stopping an already stopped scan."""
        import requests
        mock_request.side_effect = requests.HTTPError("400 Bad Request")

        with pytest.raises(requests.HTTPError):
            scans_api.stop_scan(123)


class TestScansAPIIntegration:
    """Test integration scenarios."""

    @pytest.fixture
    def scans_api(self, mock_auth):
        """Create ScansAPI instance."""
        return ScansAPI(mock_auth)

    @patch('rapid7.api.scans.BaseAPI._request')
    def test_scan_lifecycle(self, mock_request, scans_api):
        """Test complete scan lifecycle."""
        # Mock responses for different operations
        scan_id = 456
        mock_request.side_effect = [
            {"id": scan_id},  # start_site_scan returns dict, method extracts id
            {"id": scan_id, "status": "running"},  # get_scan
            {},  # pause_scan
            {},  # resume_scan
            {}   # stop_scan
        ]

        # Start scan
        result = scans_api.start_site_scan(site_id=123)
        assert result == scan_id

        # Check status
        status = scans_api.get_scan(scan_id)
        assert status['status'] == "running"

        # Pause, resume, stop
        scans_api.pause_scan(scan_id)
        scans_api.resume_scan(scan_id)
        scans_api.stop_scan(scan_id)

        # Verify all calls were made
        assert mock_request.call_count == 5
