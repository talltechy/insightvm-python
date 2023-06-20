"""
This module provides functions for loading Rapid7 InsightVM API credentials from environment variables.

Functions:
    load_r7_isvm_api_credentials: Loads the Rapid7 InsightVM API credentials from environment variables.
"""

import os
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
