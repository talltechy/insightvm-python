"""
Tests for InsightVM-Python client module.

Tests the InsightVMClient class to ensure proper initialization,
authentication handling, and API module integration.
"""
import pytest
from unittest.mock import patch, MagicMock

from rapid7.client import InsightVMClient, create_client


class TestInsightVMClient:
    """Test InsightVM client functionality."""

    def test_init_with_env_vars(self):
        """Test client initialization with environment variables."""
        client = InsightVMClient()
        assert client.auth.username == "test_user"
        assert client.auth.password == "test_pass"
        assert client.auth.base_url == "https://test.insightvm.example.com:3780"

    def test_init_with_explicit_params(self):
        """Test client initialization with explicit parameters."""
        client = InsightVMClient(
            username="custom_user",
            password="custom_pass",
            base_url="https://custom.example.com",
            verify_ssl=False,
            timeout=(5, 60)
        )
        assert client.auth.username == "custom_user"
        assert client.auth.password == "custom_pass"
        assert client.auth.base_url == "https://custom.example.com"

    def test_api_modules_initialized(self):
        """Test that all API modules are properly initialized."""
        client = InsightVMClient()

        # Check core API modules exist
        assert hasattr(client, 'assets')
        assert hasattr(client, 'asset_groups')
        assert hasattr(client, 'sites')
        assert hasattr(client, 'scans')
        assert hasattr(client, 'sonar_queries')
        assert hasattr(client, 'reports')
        assert hasattr(client, 'vulnerabilities')
        assert hasattr(client, 'solutions')

        # Check they're proper API classes
        from rapid7.api.assets import AssetAPI
        from rapid7.api.asset_groups import AssetGroupAPI
        from rapid7.api.sites import SiteAPI

        assert isinstance(client.assets, AssetAPI)
        assert isinstance(client.asset_groups, AssetGroupAPI)
        assert isinstance(client.sites, SiteAPI)

    def test_auth_passed_to_api_modules(self):
        """Test that authentication is properly passed to API modules."""
        client = InsightVMClient()

        # All API modules should have the same auth object
        assert client.assets.auth is client.auth
        assert client.asset_groups.auth is client.auth
        assert client.sites.auth is client.auth

    def test_verify_ssl_parameter(self):
        """Test SSL verification parameter handling."""
        # Test default (should be True)
        client1 = InsightVMClient()
        # Can't easily test this without accessing private attrs,
        # but at least verify the client initializes

        # Test explicit False
        client2 = InsightVMClient(verify_ssl=False)
        # Would need access to verify_ssl passed to HTTP session

        # Both should initialize successfully
        assert client1 is not None
        assert client2 is not None

    def test_timeout_parameter(self):
        """Test timeout parameter handling."""
        client = InsightVMClient(timeout=(5, 120))
        # The timeout is passed to API modules but hard to test directly
        # without accessing internal session timeout settings
        assert client is not None

    def test_repr(self):
        """Test client string representation."""
        client = InsightVMClient()
        repr_str = repr(client)
        assert "InsightVMClient" in repr_str
        assert "test.insightvm.example.com" in repr_str

    def test_context_manager(self):
        """Test client context manager functionality."""
        with InsightVMClient() as client:
            assert isinstance(client, InsightVMClient)
            assert client.auth is not None

    def test_invalid_credentials_handling(self):
        """Test handling of invalid credentials."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                InsightVMClient()
            assert "Missing InsightVM API credentials" in str(exc_info.value)


class TestCreateClient:
    """Test the create_client convenience function."""

    def test_create_client_basic(self):
        """Test basic client creation with defaults."""
        client = create_client()
        assert isinstance(client, InsightVMClient)

    def test_create_client_with_params(self):
        """Test client creation with custom parameters."""
        client = create_client(
            username="test",
            password="pass",
            base_url="https://example.com",
            verify_ssl=False
        )
        assert isinstance(client, InsightVMClient)
        assert client.auth.username == "test"
        assert client.auth.password == "pass"


class TestClientIntegration:
    """Test client integration scenarios."""

    def test_multiple_clients_isolation(self):
        """Test that multiple clients don't interfere with each other."""
        client1 = InsightVMClient(username="user1", base_url="https://server1.example.com")
        client2 = InsightVMClient(username="user2", base_url="https://server2.example.com")

        assert client1.auth.username == "user1"
        assert client2.auth.username == "user2"
        assert client1.auth.username != client2.auth.username

        assert "server1.example.com" in client1.auth.base_url
        assert "server2.example.com" in client2.auth.base_url

    def test_api_module_access_patterns(self):
        """Test typical API access patterns work."""
        client = InsightVMClient()

        # Test that we can access common patterns that users might try
        # (even if they don't make real HTTP calls due to mocking)
        assert hasattr(client.assets, 'list')
        assert hasattr(client.sites, 'create')
        assert hasattr(client.scans, 'start_site_scan')

    @pytest.mark.slow
    def test_client_lifecycle(self):
        """Test full client lifecycle (slow test marker)."""
        # This would be a slow integration test that actually makes calls
        # but since we're unit testing, we skip the actual HTTP calls
        client = InsightVMClient()

        # Test client can be created and has expected structure
        assert client.auth is not None
        assert client.assets is not None
        assert client.sites is not None

        # Test context manager works for cleanup
        with client:
            pass  # Should not raise any exceptions
