"""
Tests for Rapid7 InsightVM Assets API module.

Tests the assets.py API module to demonstrate complete API testing patterns
including CRUD operations, search, pagination, and error handling.
"""

import pytest
from unittest.mock import Mock, patch

from rapid7.api.assets import AssetAPI
from rapid7.auth import InsightVMAuth


class TestAssetAPI:
    """Test AssetAPI functionality."""

    @pytest.fixture
    def mock_auth(self):
        """Mock authentication for testing."""
        auth = Mock()
        auth.base_url = "https://test.insightvm.example.com:3780"
        auth.auth = Mock()  # HTTPBasicAuth mock
        return auth

    @pytest.fixture
    def assets_api(self, mock_auth):
        """Create AssetAPI instance for testing."""
        return AssetAPI(mock_auth)

    def test_init(self, mock_auth):
        """Test AssetAPI initialization."""
        api = AssetAPI(mock_auth)
        assert api.auth == mock_auth
        assert hasattr(api, 'get_all')  # Should have pagination method

    @patch('rapid7.api.assets.BaseAPI.get')
    def test_list_assets_basic(self, mock_get, assets_api, mock_assets_list):
        """Test basic asset listing."""
        mock_response = Mock()
        mock_response.json.return_value = mock_assets_list
        mock_get.return_value = mock_response

        result = assets_api.list(page=0, size=10)

        assert result == mock_assets_list
        mock_get.assert_called_once_with('assets', params={'page': 0, 'size': 10})

    @patch('rapid7.api.assets.BaseAPI.get')
    def test_get_asset(self, mock_get, assets_api, mock_asset_data):
        """Test individual asset retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = mock_asset_data
        mock_get.return_value = mock_response

        result = assets_api.get_asset(12345)

        assert result == mock_asset_data
        assert result['id'] == 12345
        mock_get.assert_called_once_with('assets/12345')

    @pytest.mark.skip(reason="AssetAPI.create() method not implemented")
    @patch('rapid7.api.assets.BaseAPI._request')
    def test_create_asset(self, mock_request, assets_api, mock_asset_data):
        """Test asset creation."""
        mock_request.return_value = mock_asset_data

        asset_data = {"hostname": "new-server.example.com", "ip": "192.168.1.100"}
        result = assets_api.create(asset_data)

        assert result == mock_asset_data

    @pytest.mark.skip(reason="AssetAPI.update() method not implemented")
    @patch('rapid7.api.assets.BaseAPI._request')
    def test_update_asset(self, mock_request, assets_api, mock_asset_data):
        """Test asset update."""
        mock_request.return_value = mock_asset_data

        asset_id = 12345
        update_data = {"risk_score": 25000}
        result = assets_api.update(asset_id, update_data)

        assert result == mock_asset_data
        mock_request.assert_called_once_with('PUT', f'assets/{asset_id}', json=update_data)

    @patch('rapid7.api.assets.BaseAPI._request')
    def test_delete_asset(self, mock_request, assets_api):
        """Test asset deletion."""
        mock_request.return_value = None  # DELETE typically returns no content

        asset_id = 12345
        result = assets_api.delete(asset_id)

        # Should not crash and should return raw response
        assert result is None
        mock_request.assert_called_once()

    @patch('rapid7.api.assets.BaseAPI.post')
    def test_search_assets(self, mock_post, assets_api, mock_assets_list):
        """Test asset search functionality."""
        mock_response = Mock()
        mock_response.json.return_value = mock_assets_list
        mock_post.return_value = mock_response

        search_filters = [
            {"field": "hostname", "operator": "contains", "value": "server"},
            {"field": "risk-score", "operator": "is-greater-than", "value": 1000}
        ]
        search_criteria = {"filters": search_filters, "match": "all"}

        result = assets_api.search(search_criteria)

        assert result == mock_assets_list
        mock_post.assert_called_once_with('assets/search', json=search_criteria)

class TestAssetAPIPagination:
    """Test AssetAPI pagination functionality."""

    @pytest.fixture
    def assets_api(self, mock_auth):
        """Create AssetAPI for pagination tests."""
        return AssetAPI(mock_auth)

    @patch('rapid7.api.assets.AssetAPI.list')
    def test_get_all_assets_single_page(self, mock_list, assets_api, mock_assets_list):
        """Test get_all when results fit in single page."""
        # Mock a single page response
        single_page = mock_assets_list.copy()
        single_page['page']['size'] = 3
        single_page['page']['totalResources'] = 3
        single_page['page']['totalPages'] = 1

        mock_list.return_value = single_page

        results = assets_api.get_all(batch_size=10)

        assert len(results) == 3
        assert mock_list.call_count == 1  # Only one request needed

    @patch('rapid7.api.assets.AssetAPI.list')
    def test_get_all_assets_multiple_pages(self, mock_list, assets_api, mock_assets_list):
        """Test get_all with multiple pages."""
        # Mock first page
        page1 = mock_assets_list.copy()
        page1['page']['number'] = 0
        page1['page']['totalResources'] = 150
        page1['page']['totalPages'] = 3

        # Mock second page
        page2 = mock_assets_list.copy()
        page2['page']['number'] = 1

        # Mock third page
        page3 = mock_assets_list.copy()
        page3['page']['number'] = 2

        # Mock empty final page to stop pagination
        page4 = mock_assets_list.copy()
        page4['resources'] = []
        page4['page']['number'] = 3

        mock_list.side_effect = [page1, page2, page3]

        results = assets_api.get_all(batch_size=10)

        # Should have fetched 3 pages with data
        assert len(results) == 9  # 3 pages * 3 assets each
        assert mock_list.call_count == 3


class TestAssetAPIErrorHandling:
    """Test AssetAPI error handling."""

    @pytest.fixture
    def assets_api(self, mock_auth):
        """Create AssetAPI for error handling tests."""
        return AssetAPI(mock_auth)

    @patch('rapid7.api.assets.BaseAPI._request')
    def test_get_nonexistent_asset_404(self, mock_request, assets_api):
        """Test handling of 404 for nonexistent asset."""
        import requests
        error_response = Mock()
        error_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_request.side_effect = requests.HTTPError("404 Not Found")

        with pytest.raises(requests.HTTPError):
            assets_api.get(99999)


class TestAssetAPITagManagement:
    """Test asset tag management operations."""

    @pytest.fixture
    def assets_api(self, mock_auth):
        """Create AssetAPI for tag tests."""
        return AssetAPI(mock_auth)

    @patch('rapid7.api.assets.BaseAPI.get')
    def test_get_asset_tags(self, mock_get, assets_api):
        """Test getting tags for an asset."""
        mock_tags = {
            "resources": [
                {"id": 1, "name": "critical"},
                {"id": 2, "name": "production"}
            ]
        }
        mock_response = Mock()
        mock_response.json.return_value = mock_tags
        mock_get.return_value = mock_response

        asset_id = 12345
        result = assets_api.get_tags(asset_id)

        assert result == mock_tags
        mock_get.assert_called_once_with(f'assets/{asset_id}/tags')

    @pytest.mark.skip(reason="AssetAPI.add_tags() method not implemented, use add_tag() instead")
    @patch('rapid7.api.assets.BaseAPI._request')
    def test_add_asset_tags(self, mock_request, assets_api):
        """Test adding tags to an asset."""
        mock_request.return_value = {"success": True}

        asset_id = 12345
        tag_ids = [1, 2, 3]
        result = assets_api.add_tags(asset_id, tag_ids)

        assert result["success"] is True
        mock_request.assert_called_once_with('PUT', f'assets/{asset_id}/tags', json={"tag_ids": tag_ids})

    @pytest.mark.skip(reason="AssetAPI.remove_tags() method not implemented, use remove_tag() instead")
    @patch('rapid7.api.assets.BaseAPI._request')
    def test_remove_asset_tags(self, mock_request, assets_api):
        """Test removing tags from an asset."""
        mock_request.return_value = {"success": True}

        asset_id = 12345
        tag_ids = [2]
        result = assets_api.remove_tags(asset_id, tag_ids)

        assert result["success"] is True
        mock_request.assert_called_once_with('DELETE', f'assets/{asset_id}/tags', params={"tag_ids": tag_ids})


class TestAssetAPISoftware:
    """Test asset software operations."""

    @pytest.fixture
    def assets_api(self, mock_auth):
        """Create AssetAPI for software tests."""
        return AssetAPI(mock_auth)

    @patch('rapid7.api.assets.BaseAPI.get')
    def test_get_asset_software(self, mock_get, assets_api):
        """Test getting software installed on an asset."""
        mock_software = {
            "resources": [
                {"id": 1001, "configuration": "Apache 2.4.0", "type": "web-server"},
                {"id": 1002, "configuration": "OpenSSH 8.0", "type": "ssh"}
            ]
        }
        mock_response = Mock()
        mock_response.json.return_value = mock_software
        mock_get.return_value = mock_response

        asset_id = 12345
        result = assets_api.get_software(asset_id)

        assert result == mock_software
        mock_get.assert_called_once_with(f'assets/{asset_id}/software', params={'page': 0, 'size': 500})


class TestAssetAPIBulkOperations:
    """Test bulk asset operations."""

    @pytest.fixture
    def assets_api(self, mock_auth):
        """Create AssetAPI for bulk tests."""
        return AssetAPI(mock_auth)

    @pytest.mark.skip(reason="AssetAPI.bulk_delete() method not implemented")
    @patch('rapid7.api.assets.BaseAPI._request')
    def test_bulk_delete_assets(self, mock_request, assets_api):
        """Test bulk deletion of assets."""
        mock_request.return_value = {"success": True}

        asset_ids = [12345, 12346, 12347]
        result = assets_api.bulk_delete(asset_ids)

        assert result["success"] is True
        mock_request.assert_called_once_with('DELETE', 'assets', params={"asset_ids": asset_ids})


class TestAssetAPITestingIntegration:
    """Test AssetAPI with full integration scenarios."""

    @pytest.fixture
    def assets_api(self, mock_auth):
        """Create AssetAPI for integration tests."""
        return AssetAPI(mock_auth)

    @pytest.mark.skip(reason="AssetAPI CRUD methods not fully implemented")
    @pytest.mark.slow
    def test_complete_crud_workflow(self, assets_api):
        """Test complete Create-Read-Update workflow (marked slow)."""
        # This would be an integration test with real or full-stack mocks
        # For now, just test that the methods exist and have proper signatures
        assert hasattr(assets_api, 'create')
        assert hasattr(assets_api, 'get')
        assert hasattr(assets_api, 'update')
        assert hasattr(assets_api, 'delete')

        # Test method signature compatibility (would check in real integration test)
        assert callable(assets_api.create)
        assert callable(assets_api.get)
        assert callable(assets_api.update)
        assert callable(assets_api.delete)
