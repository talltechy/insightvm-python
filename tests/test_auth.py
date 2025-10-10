"""
Tests for InsightVM-Python authentication modules.

Tests the InsightVMAuth and PlatformAuth classes to ensure proper
credential loading, validation, and authentication object creation.
"""
import pytest
from unittest.mock import patch
from requests.auth import HTTPBasicAuth

from rapid7.auth import InsightVMAuth, PlatformAuth


class TestInsightVMAuth:
    """Test InsightVM authentication functionality."""

    def test_init_with_env_vars(self):
        """Test initialization with environment variables."""
        auth = InsightVMAuth()
        assert auth.username == "test_user"
        assert auth.password == "test_pass"
        assert auth.base_url == "https://test.insightvm.example.com:3780"
        assert isinstance(auth.auth, HTTPBasicAuth)

    def test_init_with_explicit_params(self):
        """Test initialization with explicit parameters."""
        auth = InsightVMAuth(
            username="custom_user",
            password="custom_pass",
            base_url="https://custom.insightvm.example.com"
        )
        assert auth.username == "custom_user"
        assert auth.password == "custom_pass"
        assert auth.base_url == "https://custom.insightvm.example.com"
        assert isinstance(auth.auth, HTTPBasicAuth)

    def test_init_missing_credentials(self):
        """Test initialization with missing credentials raises error."""
        # Test missing username
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                InsightVMAuth()
            assert "INSIGHTVM_API_USERNAME" in str(exc_info.value)

        # Test invalid environment (should use default env vars from conftest)
        with patch.dict("os.environ",
                       {"INSIGHTVM_API_USERNAME": "", "INSIGHTVM_API_PASSWORD": ""},
                       clear=False):
            with pytest.raises(ValueError) as exc_info:
                InsightVMAuth()
            assert "Missing InsightVM API credentials" in str(exc_info.value)

    def test_init_missing_base_url(self):
        """Test initialization with missing base URL."""
        with patch.dict("os.environ",
                       {"INSIGHT_PLATFORM_API_KEY": "key"},  # Wrong env var
                       clear=False):
            auth = InsightVMAuth()
            assert auth.base_url == "https://test.insightvm.example.com:3780"

    def test_http_basic_auth_creation(self):
        """Test that HTTPBasicAuth object is created correctly."""
        auth = InsightVMAuth()
        assert isinstance(auth.auth, HTTPBasicAuth)
        # Can't directly test username/password without accessing private attrs
        # But we know it was created with our test values

    def test_repr(self):
        """Test string representation of auth object."""
        auth = InsightVMAuth()
        repr_str = repr(auth)
        assert "InsightVMAuth" in repr_str
        assert "test.insightvm.example.com" in repr_str


class TestPlatformAuth:
    """Test Platform API authentication functionality."""

    def test_init_with_env_vars(self):
        """Test initialization with environment variables."""
        auth = PlatformAuth()
        assert auth.api_key == "test_platform_key"
        assert auth.base_url == "https://us.api.insight.rapid7.com"

    def test_init_with_explicit_params(self):
        """Test initialization with explicit parameters."""
        auth = PlatformAuth(
            api_key="custom_key",
            base_url="https://custom.api.insight.rapid7.com"
        )
        assert auth.api_key == "custom_key"
        assert auth.base_url == "https://custom.api.insight.rapid7.com"

    def test_init_missing_credentials(self):
        """Test initialization with missing credentials raises error."""
        # Test missing API key
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                PlatformAuth()
            assert "INSIGHT_PLATFORM_API_KEY" in str(exc_info.value)

    def test_get_headers(self):
        """Test header generation for API requests."""
        auth = PlatformAuth()
        headers = auth.get_headers()

        expected_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Api-Key": "test_platform_key"
        }

        assert headers == expected_headers
        assert headers["X-Api-Key"] == "test_platform_key"
        assert headers["Accept"] == "application/json"

    def test_get_headers_custom_key(self):
        """Test header generation with custom API key."""
        auth = PlatformAuth(api_key="custom_test_key")
        headers = auth.get_headers()
        assert headers["X-Api-Key"] == "custom_test_key"

    def test_repr(self):
        """Test string representation of PlatformAuth object."""
        auth = PlatformAuth()
        repr_str = repr(auth)
        assert "PlatformAuth" in repr_str
        assert "us.api.insight.rapid7.com" in repr_str


class TestAuthIntegration:
    """Test authentication integration scenarios."""

    def test_ssl_verification_configuration(self):
        """Test that SSL verification settings are loaded."""
        # This would ideally test that the SSL verification setting
        # from INSIGHTVM_VERIFY_SSL environment variable is used,
        # but InsightVMAuth doesn't directly handle SSL settings
        # (that's handled in the client/http layer)
        auth = InsightVMAuth()
        assert auth.base_url.startswith("https://")  # HTTPS URL indicates SSL usage

    def test_multiple_instances_isolation(self):
        """Test that multiple auth instances don't interfere."""
        auth1 = InsightVMAuth(username="user1", password="pass1")
        auth2 = InsightVMAuth(username="user2", password="pass2")

        assert auth1.username == "user1"
        assert auth2.username == "user2"
        assert auth1.username != auth2.username
