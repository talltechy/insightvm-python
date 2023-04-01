import unittest
from unittest.mock import patch
import pa_cortex_xdr_r7_insightvm_asset_compare as script

class TestPaCortexXdrR7InsightvmAssetCompare(unittest.TestCase):

    def test_xdr_advanced_authentication(self):
        xdr_api_key = "test_api_key"
        xdr_api_key_id = "1234"
        headers = script.xdr_advanced_authentication(xdr_api_key, xdr_api_key_id)
        
        self.assertIn("Authorization", headers)
        self.assertIn("x-xdr-nonce", headers)
        self.assertIn("x-xdr-timestamp", headers)
        self.assertIn("x-xdr-auth-id", headers)
        self.assertEqual(headers["x-xdr-auth-id"], "1234")

    @patch("requests.head")
    def test_check_base_url(self, mock_head):
        mock_head.return_value.status_code = 200

        base_url = "https://example.com"
        headers = {"Authorization": "test_auth_token"}

        result = script.check_base_url(base_url, headers)
        self.assertEqual(result, "Connected to https://example.com with status code 200")

    @patch("requests.post")
    def test_search_insightvm_hostname(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '{"resources": [{"id": 1, "hostname": "test-host"}]}'

        base_url = "https://example.com"
        headers = {"Authorization": "test_auth_token"}
        hostname = "test-host"

        result = script.search_insightvm_hostname(base_url, headers, hostname)
        self.assertEqual(result, [{"id": 1, "hostname": "test-host"}])

    @patch("requests.post")
    def test_search_insightvm_hostname_error(self, mock_post):
        mock_post.return_value.status_code = 500

        base_url = "https://example.com"
        headers = {"Authorization": "test_auth_token"}
        hostname = "test-host"

        result = script.search_insightvm_hostname(base_url, headers, hostname)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
