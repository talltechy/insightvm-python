"""
This module provides functions for loading Rapid7 InsightVM API credentials from environment variables.

Functions:
    load_r7_isvm_api_credentials: Loads the Rapid7 InsightVM API credentials from environment variables.
    get_isvm_api_headers: Returns the headers required to make API requests.
"""

import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


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


def get_isvm_api_headers():
    """
    Returns the headers required to make API requests.

    Returns:
    Dictionary containing the headers required to make API requests.
    """
    isvm_api_username, isvm_api_password, _ = load_r7_isvm_api_credentials()

    isvm_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Basic "
        + base64.b64encode(
            f"{isvm_api_username}:{isvm_api_password}".encode("utf-8")
        ).decode("utf-8"),
    }

    return isvm_headers
