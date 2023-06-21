"""
This module provides functions for interacting with the InsightVM API.
"""

from typing import Optional, List, Dict, Any
import requests
from platform.rapid7.api_r7_auth import load_r7_isvm_api_credentials, get_isvm_api_headers

# Load the InsightVM API credentials
(
    isvm_api_username,
    isvm_api_password,
    isvm_base_url,
) = load_r7_isvm_api_credentials()

# Load the ISVM API headers
isvm_headers = get_isvm_api_headers()


def search_asset_isvm(base_url: str, headers: dict, hostname: str, verify: bool = False) -> Optional[List[Dict[str, Any]]]:
    """
    Search for a hostname in the InsightVM API.

    :param base_url: Base URL for the InsightVM API
    :param headers: Headers for the InsightVM API request
    :param hostname: Hostname to search for
    :param verify: Whether to verify SSL certificates (default: False)
    :return: Matching assets (list of dictionaries) or None if there is an error
    """
    url = f"{base_url}/api/3/assets/search"
    body = {
        "match": "all",
        "filters": [{"field": "host-name", "operator": "is", "value": hostname}],
    }
    response = requests.post(url, headers=headers, json=body, timeout=10, verify=verify)

    if response.status_code != 200:
        print(f"Error searching for hostname {hostname} in InsightVM")
        return None

    data = response.json()
    return data.get("resources", [])

def get_asset_isvm(base_url: str, headers: dict, asset_id: str, verify: bool = False) -> Optional[Dict[str, Any]]:
    """
    Get an asset by ID from the InsightVM API.

    :param base_url: Base URL for the InsightVM API
    :param headers: Headers for the InsightVM API request
    :param asset_id: ID of the asset to retrieve
    :param verify: Whether to verify SSL certificates (default: False)
    :return: Asset (dictionary) or None if there is an error
    """
    url = f"{base_url}/api/3/assets/{asset_id}"
    response = requests.get(url, headers=headers, timeout=10, verify=verify)

    if response.status_code != 200:
        print(f"Error retrieving asset {asset_id} from InsightVM")
        return None

    data = response.json()
    return data

def get_assets_isvm(base_url: str, headers: dict, page: int = 1, page_size: int = 10, verify: bool = False) -> Optional[Dict[str, Any]]:
    """
    Get a list of assets from the InsightVM API.

    :param base_url: Base URL for the InsightVM API
    :param headers: Headers for the InsightVM API request
    :param page: Page number to retrieve (default: 1)
    :param page_size: Number of assets to retrieve per page (default: 10)
    :param verify: Whether to verify SSL certificates (default: False)
    :return: List of assets (dictionary) or None if there is an error
    """
    url = base_url + "/api/3/assets"
    params = {
        "page": page,
        "page_size": page_size,
    }
    response = requests.get(url, headers=headers, params=params, timeout=10, verify=verify)

    if response.status_code != 200:
        print("Error retrieving assets from InsightVM")
        return None

    data = response.json()
    return data
