# import requests
# import json
import base64
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Python script that uses the Palo Alto Cortex XDR API and Rapid7 InsightVM API
# This script is provided as-is without warranty of any kind.
# Palo Alto Networks and Rapid7 do not support this script.
# Use at your own risk.
# Written by Matt Wyen (https://github.com/talltechy)


def get_xdr_credentials():
    """
    Returns the Cortex XDR API credentials from environment variables.

    Returns:
    Tuple containing the XDR API key, XDR API key ID, and XDR base URL.
    """
    return (
        os.getenv("XDR_API_KEY"),
        os.getenv("XDR_API_KEY_ID"),
        os.getenv("XDR_BASE_URL"),
    )


def get_insightvm_credentials():
    """
    Returns the InsightVM API credentials from environment variables.

    Returns:
    Tuple containing the InsightVM API key, InsightVM API secret, and InsightVM base URL.
    """
    insightvm_api_key = os.getenv("INSIGHTVM_API_KEY")
    insightvm_api_secret = os.getenv("INSIGHTVM_API_SECRET")
    insightvm_base_url = os.getenv("INSIGHTVM_BASE_URL")
    return insightvm_api_key, insightvm_api_secret, insightvm_base_url


def get_xdr_headers(api_key, api_secret):
    """
    Sets up XDR request headers.

    Args:
    api_key: The XDR API key.
    api_secret: The XDR API secret.

    Returns:
    Dictionary containing the XDR request headers.
    """
    headers = {
        "x-xdr-auth-id": api_key,
        "x-xdr-auth-token": api_secret,
        "Content-Type": "application/json",
    }
    return headers


def get_insightvm_headers(api_key, api_secret):
    """
    Sets up InsightVM request headers.

    Args:
    api_key: The InsightVM API key.
    api_secret: The InsightVM API secret.

    Returns:
    Dictionary containing the InsightVM request headers.
    """
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Basic "
        + base64.b64encode(f"{api_key}:{api_secret}".encode("utf-8")).decode("utf-8"),
    }
    return headers
