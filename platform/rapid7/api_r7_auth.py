"""
This module provides functions for loading Rapid7 InsightVM API credentials from environment variables.

Functions:
    load_r7_platform_api_credentials: Loads the Rapid7 Insight Platform API credentials from environment variables.
    load_r7_isvm_api_credentials: Loads the Rapid7 InsightVM API credentials from environment variables.
    get_platform_api_headers: Returns the headers required to make Insight Platform API requests.
"""

import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()

def load_r7_platform_api_credentials():
    """
    Loads the Rapid7 Insight Platform API credentials from environment variables.

    Returns:
    Tuple containing the Insight Platform API key and base URL.
    Raises:
    ValueError: If any of the required environment variables are missing.
    """
    r7_platform_api_key = os.getenv('INSIGHT_PLATFORM_API_KEY')
    r7_platform_base_url = os.getenv('INSIGHT_PLATFORM_BASE_URL')

    if not r7_platform_api_key or not r7_platform_base_url:
        raise ValueError("Missing Insight Platform API credentials or BASE URL. Please check .env file.")

    return r7_platform_api_key, r7_platform_base_url

def get_platform_api_headers():
    """
    Returns the headers required to make Insight Platform API requests.

    Returns:
    Dictionary containing the headers required to make Insight Platform API requests.
    """
    r7_platform_api_key, _ = load_r7_platform_api_credentials()

    platform_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Key": r7_platform_api_key,
    }

    return platform_headers

def load_r7_isvm_api_credentials():
    """
    Loads the Rapid7 InsightVM API credentials from environment variables.

    Returns:
    Tuple containing the ISVM API key and API key ID.
    Raises:
    ValueError: If any of the required environment variables are missing.
    """
    isvm_api_username = os.getenv('INSIGHTVM_API_USERNAME')
    isvm_api_password = os.getenv('INSIGHTVM_API_PASSWORD')
    isvm_base_url = os.getenv('INSIGHTVM_BASE_URL')

    if not isvm_api_username or not isvm_api_password or not isvm_base_url:
        raise ValueError("Missing ISVM API credentials or BASE URL. Please check .env file.")

    return isvm_api_username, isvm_api_password, isvm_base_url

def isvm_get_access_token():
    """
    Generates an access token for the Rapid7 InsightVM API.

    Returns:
    The access token as a string.
    """
    isvm_api_username, isvm_api_password, isvm_base_url = load_r7_isvm_api_credentials()

    # Construct the URL for the access token endpoint
    token_url = f"{isvm_base_url}/api/3/access-tokens"

    # Make a POST request to the access token endpoint to generate a new access token
    response = requests.post(
        token_url,
        auth=HTTPBasicAuth(isvm_api_username, isvm_api_password),
        headers={"Accept": "application/json"},
        timeout=10 # Add a timeout argument to avoid hanging indefinitely
    )

    # Check if the request was successful
    if response.status_code != 201:
        raise ValueError("Failed to generate access token.")

    # Extract the access token from the response
    access_token = response.json()["token"]

    return access_token
