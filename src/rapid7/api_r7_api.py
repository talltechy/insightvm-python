"""
TODO: Add docstring
"""

import collections
from typing import Any, Tuple
import logging
import urllib3
import requests
from src.rapid7.api_r7_auth_class import R7_ISVM_Auth

# Set up logging
logging.basicConfig(filename="api_r7_api.log", level=logging.ERROR)


class R7_ISVM_Api:
    def __init__(
        self, auth: R7_ISVM_Auth, fqdn: str, api_name: str, timeout: Tuple[int, int]
    ) -> None:
        self.auth = auth
        self.fqdn = fqdn
        self.api_name = api_name
        self.timeout = timeout

    def _get_api_url(self, call_name: str) -> str:
        """
        Returns the API URL.

        Returns:
            A string containing the API URL.
        """
        return f"{self.auth.isvm_base_url}/api/3/{self.api_name}/{call_name}"

    def _call(
        self,
        call_name: str,
        method: str = "post",
        params: dict = None,
        json_value: object = None,
        header_params=None,
    ) -> requests.Response:
        """
        Calls the API with the specified parameters.

        Args:
            call_name: A string containing the name of the API call to make.
            method: A string containing the HTTP method to use for the API call (default is "post").
            params: A dictionary containing the query parameters to include in the API call (default is None).
            json_value: An object containing the JSON data to include in the API call (default is None).
            header_params: A dictionary containing additional headers to include in the API call (default is None).

        Returns:
            A requests.Response object containing the API response.
        """
        if header_params is None:
            header_params = {}
        if params is None:
            params = {}
        if json_value is None:
            json_value = {}
        url = self._get_api_url(call_name)
        headers = self.auth.get_isvm_encoded_auth_header()
        self.extend_dict(headers, header_params)

        return self._execute_call(
            url=url,
            method=method,
            params=params,
            json_value=json_value,
            headers=headers,
        )

    def _execute_call(
        self,
        url: str,
        method: str,
        params: dict = None,
        json_value: object = None,
        headers: dict = None,
    ) -> requests.Response:
        """
        Executes the API call.

        Returns:
            A requests.Response object containing the API response.
        """
        response = None
        if method == "get":
            response = requests.get(
                url, headers=headers, params=params, timeout=self.timeout
            )
        elif method == "post":
            response = requests.post(
                url, headers=headers, json=json_value, timeout=self.timeout
            )
        elif method == "put":
            response = requests.put(
                url, headers=headers, json=json_value, timeout=self.timeout
            )
        elif method == "delete":
            response = requests.delete(url, headers=headers, timeout=self.timeout)
        if response is not None:
            response.raise_for_status()
        else:
            response = requests.Response()
        return response

    @staticmethod
    def extend_dict(*args):
        """
        Extends a dictionary with the key-value pairs from one or more dictionaries.

        Args:
            *args: One or more dictionaries to extend.

        Returns:
            A dictionary containing the extended key-value pairs.
        """
        if args is not None:
            if type(args[0]) is collections.OrderedDict:
                result = collections.OrderedDict()
            else:
                result = {}
            for arg in args:
                result.update(arg)
            return result
        return {}
