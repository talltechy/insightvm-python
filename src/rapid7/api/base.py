"""
Base API client for InsightVM API operations.

This module provides a base class that all API operation classes inherit from,
providing consistent request handling, error management, and SSL configuration.
"""

import os
import logging
from typing import Optional, Dict, Any, Tuple
import urllib3
import requests


# Set up logging
logging.basicConfig(filename='rapid7_api.log', level=logging.ERROR)


class BaseAPI:
    """
    Base class for all InsightVM API operations.

    This class provides common functionality for making API requests,
    including authentication, SSL verification, timeout handling, and
    consistent error management.

    Attributes:
        auth: Authentication object with .auth property (HTTPBasicAuth)
        base_url (str): Base URL for the InsightVM API
        verify_ssl (bool): Whether to verify SSL certificates
        timeout (tuple): Timeout values (connect_timeout, read_timeout)

    Example:
        >>> from src.rapid7.auth import InsightVMAuth
        >>> auth = InsightVMAuth()
        >>> api = BaseAPI(auth)
        >>> response = api.get('assets')
    """

    def __init__(
        self,
        auth,
        verify_ssl: Optional[bool] = None,
        timeout: Tuple[int, int] = (10, 90)
    ):
        """
        Initialize the base API client.

        Args:
            auth: Authentication object (InsightVMAuth instance)
            verify_ssl: Whether to verify SSL certificates (default: from env or True)
            timeout: Tuple of (connect_timeout, read_timeout) in seconds
        """
        self.auth = auth
        self.base_url = auth.base_url
        self.timeout = timeout

        # SSL verification configuration
        if verify_ssl is None:
            env_verify = os.getenv('INSIGHTVM_VERIFY_SSL', 'true').lower()
            self.verify_ssl = env_verify in ('true', '1', 'yes')
        else:
            self.verify_ssl = verify_ssl

        # Suppress urllib3 warnings when SSL verification is disabled
        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _build_url(self, endpoint: str) -> str:
        """
        Build full API URL from endpoint.

        Args:
            endpoint: API endpoint (e.g., 'assets', 'sites/123')

        Returns:
            Full URL for the API request
        """
        # Remove leading slash if present
        endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/api/3/{endpoint}"

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        return_raw: bool = False,
        **kwargs
    ) -> Any:
        """
        Make an API request with automatic JSON parsing.

        By default, this method returns parsed JSON dictionaries. For endpoints
        that return binary content (like file downloads), use return_raw=True.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            params: Query parameters
            json: JSON body data
            headers: Additional headers
            return_raw: If True, return raw Response object instead of parsed JSON
                       (useful for binary content like downloads). Default: False
            **kwargs: Additional arguments for requests

        Returns:
            Parsed JSON dictionary if return_raw=False (default),
            or raw Response object if return_raw=True

        Raises:
            requests.HTTPError: If the request fails

        Example:
            >>> # Standard JSON response
            >>> data = self._request('GET', 'assets')
            >>> print(data['resources'])
            >>>
            >>> # Binary content (e.g., file download)
            >>> response = self._request('GET', 'reports/1/download', return_raw=True)
            >>> content = response.content
        """
        url = self._build_url(endpoint)

        # Set defaults
        kwargs.setdefault('auth', self.auth.auth)
        kwargs.setdefault('verify', self.verify_ssl)
        kwargs.setdefault('timeout', self.timeout)

        if params:
            kwargs['params'] = params
        if json:
            kwargs['json'] = json
        if headers:
            kwargs['headers'] = headers

        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()

            # Return raw response for binary content, parsed JSON otherwise
            if return_raw:
                return response

            # Parse JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            logging.error("%s %s failed: %s", method, url, str(e))
            raise

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make a GET request (returns raw Response for backward compatibility).

        Note: For new code, prefer using _request() directly which returns
        parsed JSON by default.

        Args:
            endpoint: API endpoint
            params: Query parameters
            **kwargs: Additional arguments

        Returns:
            Response object (for backward compatibility with existing code)
        """
        return self._request(
            'GET', endpoint, params=params, return_raw=True, **kwargs
        )

    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make a POST request (returns raw Response for backward compatibility).

        Note: For new code, prefer using _request() directly which returns
        parsed JSON by default.

        Args:
            endpoint: API endpoint
            json: JSON body data
            **kwargs: Additional arguments

        Returns:
            Response object (for backward compatibility with existing code)
        """
        return self._request(
            'POST', endpoint, json=json, return_raw=True, **kwargs
        )

    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make a PUT request (returns raw Response for backward compatibility).

        Note: For new code, prefer using _request() directly which returns
        parsed JSON by default.

        Args:
            endpoint: API endpoint
            json: JSON body data
            **kwargs: Additional arguments

        Returns:
            Response object (for backward compatibility with existing code)
        """
        return self._request(
            'PUT', endpoint, json=json, return_raw=True, **kwargs
        )

    def delete(
        self,
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        Make a DELETE request (returns raw Response for backward compatibility).

        Note: For new code, prefer using _request() directly which returns
        parsed JSON by default.

        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments

        Returns:
            Response object (for backward compatibility with existing code)
        """
        return self._request(
            'DELETE', endpoint, return_raw=True, **kwargs
        )
