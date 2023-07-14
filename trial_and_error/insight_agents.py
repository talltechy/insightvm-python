"""
This module provides functions for retrieving a list of all agents using the Insight Platform API.
"""

import requests
from src.rapid7.api_r7_auth import load_r7_platform_api_credentials, get_platform_api_headers

def get_insight_agents(page=1, page_size=50):
    """
    Returns a list of all agents using the Insight Platform API.

    Args:
    page (int): The page number to retrieve. Default is 1.
    page_size (int): The number of items to retrieve per page. Default is 50.

    Returns:
    List containing all agents.
    """
    url = f"{load_r7_platform_api_credentials()[1]}/api/endpoint_agent"
    headers = get_platform_api_headers()

    params = {
        "page": page,
        "size": page_size
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)

    if response.status_code != 200:
        raise ValueError(f"Failed to get agents. Status code: {response.status_code}")

    return response.json()
