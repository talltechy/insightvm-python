"""
Tests for Rapid7 InsightVM Reports API module.

Tests the reports.py API module for report generation and management.
"""

import pytest
from unittest.mock import Mock, patch

from rapid7.api.reports import ReportsAPI


class TestReportsAPI:
    """Test ReportsAPI functionality."""

    @pytest.fixture
    def mock_auth(self):
        """Mock authentication for testing."""
        auth = Mock()
        auth.base_url = "https://test.insightvm.example.com:3780"
        auth.auth = Mock()
        return auth

    @pytest.fixture
    def reports_api(self, mock_auth):
        """Create ReportsAPI instance for testing."""
        return ReportsAPI(mock_auth)

    def test_init(self, mock_auth):
        """Test ReportsAPI initialization."""
        api = ReportsAPI(mock_auth)
        assert api.auth == mock_auth
        assert hasattr(api, 'MAX_PAGE_SIZE')
        assert api.MAX_PAGE_SIZE == 500

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_list_reports(self, mock_request, reports_api):
        """Test listing all reports."""
        mock_response = {
            "resources": [
                {"id": 1, "name": "Vulnerability Report", "format": "pdf"},
                {"id": 2, "name": "Compliance Report", "format": "html"}
            ],
            "page": {"number": 0, "size": 10}
        }
        mock_request.return_value = mock_response

        result = reports_api.list(page=0, size=10)

        assert result == mock_response
        assert len(result['resources']) == 2
        mock_request.assert_called_once()

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_get_report(self, mock_request, reports_api):
        """Test getting a specific report configuration."""
        report_id = 123
        mock_response = {
            "id": report_id,
            "name": "Monthly Security Report",
            "format": "pdf",
            "template": "vulnerability-report"
        }
        mock_request.return_value = mock_response

        result = reports_api.get_report(report_id)

        assert result == mock_response
        assert result['id'] == report_id
        mock_request.assert_called_once_with('GET', f'reports/{report_id}')

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_create_report(self, mock_request, reports_api):
        """Test creating a new report configuration."""
        report_config = {
            "name": "New Report",
            "format": "pdf",
            "template": "audit-report",
            "scope": {"sites": [1, 2, 3]}
        }
        mock_response = {"id": 456, **report_config}
        mock_request.return_value = mock_response

        result = reports_api.create(report_config)

        assert result == mock_response
        assert result['id'] == 456
        call_args = mock_request.call_args
        assert call_args[0][0] == 'POST'
        assert call_args[1]['json'] == report_config

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_update_report(self, mock_request, reports_api):
        """Test updating a report configuration."""
        report_id = 123
        updates = {"name": "Updated Report Name"}
        mock_response = {"id": report_id, **updates}
        mock_request.return_value = mock_response

        result = reports_api.update(report_id, updates)

        assert result == mock_response
        call_args = mock_request.call_args
        assert call_args[0][0] == 'PUT'
        assert f'reports/{report_id}' in call_args[0][1]

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_delete_report(self, mock_request, reports_api):
        """Test deleting a report configuration."""
        report_id = 123
        mock_request.return_value = {}

        result = reports_api.delete_report(report_id)

        mock_request.assert_called_once_with('DELETE', f'reports/{report_id}')

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_generate_report(self, mock_request, reports_api):
        """Test generating a report."""
        report_id = 123
        mock_response = {"id": "instance-789"}  # API returns dict
        mock_request.return_value = mock_response

        result = reports_api.generate(report_id)

        assert result == "instance-789"  # Method extracts and converts to string
        call_args = mock_request.call_args
        assert call_args[0][0] == 'POST'
        assert f'reports/{report_id}/generate' in call_args[0][1]

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_get_report_instance(self, mock_request, reports_api):
        """Test getting a report instance."""
        report_id = 123
        instance_id = "instance-789"
        mock_response = {
            "id": instance_id,
            "status": "complete",
            "uri": "/reports/123/history/instance-789"
        }
        mock_request.return_value = mock_response

        result = reports_api.get_instance(report_id, instance_id)

        assert result == mock_response
        assert result['status'] == "complete"

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_download_report(self, mock_request, reports_api):
        """Test downloading a report."""
        report_id = 123
        instance_id = "instance-789"
        mock_content = b"PDF report content"
        
        mock_response = Mock()
        mock_response.content = mock_content
        mock_request.return_value = mock_response

        result = reports_api.download(report_id, instance_id)

        assert result == mock_content  # Method returns response.content (bytes)
        call_args = mock_request.call_args
        # Verify return_raw=True for binary content
        assert call_args[1].get('return_raw') is True

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_get_templates(self, mock_request, reports_api):
        """Test listing available report templates."""
        mock_response = {
            "resources": [
                {"id": "audit-report", "name": "Audit Report"},
                {"id": "vulnerability-report", "name": "Vulnerability Report"}
            ]
        }
        mock_request.return_value = mock_response

        result = reports_api.get_templates()

        assert result == mock_response
        assert len(result['resources']) == 2

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_list_with_pagination(self, mock_request, reports_api):
        """Test list respects page size limits."""
        mock_response = {"resources": [], "page": {}}
        mock_request.return_value = mock_response

        # Request larger than MAX_PAGE_SIZE
        reports_api.list(page=0, size=1000)

        call_args = mock_request.call_args
        # Should be capped at MAX_PAGE_SIZE (500)
        assert call_args[1]['params']['size'] == 500


class TestReportsAPIHistory:
    """Test report history operations."""

    @pytest.fixture
    def reports_api(self, mock_auth):
        """Create ReportsAPI instance."""
        return ReportsAPI(mock_auth)

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_get_report_history(self, mock_request, reports_api):
        """Test getting report generation history."""
        report_id = 123
        mock_response = {
            "resources": [
                {"id": "instance-1", "status": "complete", "generated": "2025-01-01"},
                {"id": "instance-2", "status": "complete", "generated": "2025-01-02"}
            ]
        }
        mock_request.return_value = mock_response

        result = reports_api.get_history(report_id)

        assert result == mock_response
        assert len(result['resources']) == 2
        call_args = mock_request.call_args
        assert f'reports/{report_id}/history' in call_args[0][1]


class TestReportsAPIFormats:
    """Test report format operations."""

    @pytest.fixture
    def reports_api(self, mock_auth):
        """Create ReportsAPI instance."""
        return ReportsAPI(mock_auth)

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_get_formats(self, mock_request, reports_api):
        """Test getting available report formats."""
        mock_response = {
            "resources": [
                {"id": "pdf", "name": "PDF"},
                {"id": "html", "name": "HTML"},
                {"id": "csv", "name": "CSV"}
            ]
        }
        mock_request.return_value = mock_response

        result = reports_api.get_formats()

        assert result == mock_response
        assert len(result['resources']) == 3


class TestReportsAPIErrorHandling:
    """Test error handling in ReportsAPI."""

    @pytest.fixture
    def reports_api(self, mock_auth):
        """Create ReportsAPI instance."""
        return ReportsAPI(mock_auth)

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_get_nonexistent_report(self, mock_request, reports_api):
        """Test handling of 404 for nonexistent report."""
        import requests
        mock_request.side_effect = requests.HTTPError("404 Not Found")

        with pytest.raises(requests.HTTPError):
            reports_api.get_report(99999)

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_generate_with_invalid_config(self, mock_request, reports_api):
        """Test generating report with invalid configuration."""
        import requests
        mock_request.side_effect = requests.HTTPError("400 Bad Request")

        with pytest.raises(requests.HTTPError):
            reports_api.generate(123)


class TestReportsAPIIntegration:
    """Test integration scenarios."""

    @pytest.fixture
    def reports_api(self, mock_auth):
        """Create ReportsAPI instance."""
        return ReportsAPI(mock_auth)

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_report_creation_and_generation(self, mock_request, reports_api):
        """Test complete report workflow."""
        # Mock responses for different operations
        report_config = {"name": "Test Report", "format": "pdf"}
        report_id = 456
        instance_id = "instance-789"
        
        mock_request.side_effect = [
            {"id": report_id},  # create
            {"id": instance_id},  # generate returns dict, method extracts id as string
            {"id": instance_id, "status": "complete"},  # get_instance
            Mock(content=b"PDF content")  # download returns Response with content
        ]

        # Create report
        created = reports_api.create(report_config)
        assert created['id'] == report_id

        # Generate report
        instance = reports_api.generate(report_id)
        assert instance == instance_id

        # Check status
        status = reports_api.get_instance(report_id, instance_id)
        assert status['status'] == "complete"

        # Download report
        content = reports_api.download(report_id, instance_id)
        assert content == b"PDF content"  # download returns bytes

        # Verify all calls were made
        assert mock_request.call_count == 4

    @patch('rapid7.api.reports.BaseAPI._request')
    def test_report_update_and_delete(self, mock_request, reports_api):
        """Test report update and deletion."""
        report_id = 123
        
        mock_request.side_effect = [
            {"id": report_id, "name": "Updated Name"},  # update
            {}  # delete_report
        ]

        # Update report
        updated = reports_api.update(report_id, {"name": "Updated Name"})
        assert updated['name'] == "Updated Name"

        # Delete report
        reports_api.delete_report(report_id)

        # Verify both calls were made
        assert mock_request.call_count == 2
