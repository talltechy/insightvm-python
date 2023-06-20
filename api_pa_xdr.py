"""
This module provides functions to interact with the Cortex XDR API.
"""

import json
import logging
from typing import Optional
import requests
from dotenv import load_dotenv
from api_pa_xdr_auth import generate_advanced_authentication, load_xdr_api_credentials

# Load environment variables from .env file
load_dotenv(".env")

# Load the XDR API credentials
xdr_api_key, xdr_api_key_id, xdr_base_url = load_xdr_api_credentials()

# Call the `generate_advanced_authentication()` function with the loaded credentials
auth_headers: dict[str, str] = generate_advanced_authentication(
    api_key=xdr_api_key, api_key_id=xdr_api_key_id
)

# Define the base URL for the Cortex XDR API
BASE_URL = xdr_base_url

# Set up logging
logging.basicConfig(filename='api_pa_xdr.log', level=logging.ERROR)

def get_incidents(query: Optional[str] = None):
    """
    Retrieves a list of incidents from the Cortex XDR API.

    Args:
    query: Optional string containing the query to filter the incidents.

    Returns:
    List of incidents.
    """
    # Define the endpoint URL
    endpoint_url: str = f"{BASE_URL}/incidents"

    # Define the query parameters
    params = {}
    if query:
        params["query"] = query

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.get(
            endpoint_url, headers=auth_headers, params=params, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the list of incidents
        return response_json["reply"]

    except requests.exceptions.RequestException as error:
        logging.error("Error getting incidents: %s", str(error))
        return []

def get_endpoints(query: Optional[str] = None):
    """
    Retrieves a list of endpoints from the Cortex XDR API.

    Args:
    query: Optional string containing the query to filter the endpoints.

    Returns:
    List of endpoints.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/endpoints"

    # Define the query parameters
    params = {}
    if query:
        params["query"] = query

    # Send the API request with a timeout of 10 seconds
    response = requests.get(
        endpoint_url, headers=auth_headers, params=params, timeout=10
    )

    # Raise an exception if the request fails
    response.raise_for_status()

    # Parse the response JSON
    response_json = response.json()

    # Return the list of endpoints
    return response_json["reply"]

def get_alerts(query: Optional[str] = None):
    """
    Retrieves a list of alerts from the Cortex XDR API.

    Args:
    query: Optional string containing the query to filter the alerts.

    Returns:
    List of alerts.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/alerts"

    # Define the query parameters
    params = {}
    if query:
        params["query"] = query

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.get(
            endpoint_url, headers=auth_headers, params=params, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the list of alerts
        return response_json["reply"]

    except requests.exceptions.RequestException as error:
        logging.error("Error getting alerts: %s", error)
        return []
