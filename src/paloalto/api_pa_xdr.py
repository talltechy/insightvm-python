"""
This module provides functions to interact with the Cortex XDR API.

Functions:
- get_incidents(query: Optional[str] = None) -> List[dict]: Retrieves a list of incidents from the Cortex XDR API.
- get_endpoints(query: Optional[str] = None) -> List[dict]: Retrieves a list of endpoints from the Cortex XDR API.
- get_alerts(query: Optional[str] = None) -> List[dict]: Retrieves a list of alerts from the Cortex XDR API.
- get_endpoint_details(endpoint_id: str) -> dict: Retrieves details for a specific endpoint from the Cortex XDR API.
- get_incident_details(incident_id: str) -> dict: Retrieves details for a specific incident from the Cortex XDR API.
- get_alert_details(alert_id: str) -> dict: Retrieves details for a specific alert from the Cortex XDR API.
- isolate_endpoint(endpoint_id: str) -> dict: Isolates an endpoint from the Cortex XDR API.
- unisolate_endpoint(endpoint_id: str) -> dict: Unisolates an endpoint from the Cortex XDR API.
- get_endpoint_quarantine_status(endpoint_id: str) -> dict: Retrieves the quarantine status for a specific endpoint from the Cortex XDR API.
- quarantine_endpoint(endpoint_id: str) -> dict: Quarantines an endpoint from the Cortex XDR API.
- unquarantine_endpoint(endpoint_id: str) -> dict: Unquarantines an endpoint from the Cortex XDR API.
- get_endpoint_network_details(endpoint_id: str) -> dict: Retrieves network details for a specific endpoint from the Cortex XDR API.
"""

import json
import logging
from typing import Optional, List
import requests
from dotenv import load_dotenv
from src.paloalto.cortex_xdr.api_pa_xdr_auth import generate_advanced_authentication, load_xdr_api_credentials

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

def get_incidents(query: Optional[str] = None) -> List[dict]:
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

def get_endpoints(query: Optional[str] = None) -> List[dict]:
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

def get_alerts(query: Optional[str] = None) -> List[dict]:
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

def get_endpoint_details(endpoint_id: str) -> dict:
    """
    Retrieves details for a specific endpoint from the Cortex XDR API.

    Args:
    endpoint_id: The ID of the endpoint to retrieve details for.

    Returns:
    Dictionary containing the endpoint details.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/endpoints/{endpoint_id}"

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.get(
            endpoint_url, headers=auth_headers, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the endpoint details
        return response_json["reply"]

    except requests.exceptions.RequestException as error:
        logging.error("Error getting endpoint details: %s", error)
        return {}

def get_incident_details(incident_id: str) -> dict:
    """
    Retrieves details for a specific incident from the Cortex XDR API.

    Args:
    incident_id: The ID of the incident to retrieve details for.

    Returns:
    Dictionary containing the incident details.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/incidents/{incident_id}"

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.get(
            endpoint_url, headers=auth_headers, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the incident details
        return response_json["reply"]

    except requests.exceptions.RequestException as error:
        logging.error("Error getting incident details: %s", error)
        return {}

def get_alert_details(alert_id: str) -> dict:
    """
    Retrieves details for a specific alert from the Cortex XDR API.

    Args:
    alert_id: The ID of the alert to retrieve details for.

    Returns:
    Dictionary containing the alert details.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/alerts/{alert_id}"

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.get(
            endpoint_url, headers=auth_headers, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the alert details
        return response_json["reply"]

    except requests.exceptions.RequestException as error:
        logging.error("Error getting alert details: %s", error)
        return {}

def isolate_endpoint(endpoint_id: str) -> dict:
    """
    Isolates an endpoint from the Cortex XDR API.

    Args:
    endpoint_id: The ID of the endpoint to isolate.

    Returns:
    Dictionary containing the response from the Cortex XDR API.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/endpoints/isolate"

    # Define the request body
    request_body = {
        "request_data": {
            "endpoint_id": endpoint_id
        }
    }

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.post(
            endpoint_url, headers=auth_headers, json=request_body, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the response from the Cortex XDR API
        return response_json

    except requests.exceptions.RequestException as error:
        logging.error("Error isolating endpoint: %s", error)
        return {}

def unisolate_endpoint(endpoint_id: str) -> dict:
    """
    Unisolates an endpoint from the Cortex XDR API.

    Args:
    endpoint_id: The ID of the endpoint to unisolate.

    Returns:
    Dictionary containing the response from the Cortex XDR API.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/endpoints/unisolate"

    # Define the request body
    request_body = {
        "request_data": {
            "endpoint_id": endpoint_id
        }
    }

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.post(
            endpoint_url, headers=auth_headers, json=request_body, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the response from the Cortex XDR API
        return response_json

    except requests.exceptions.RequestException as error:
        logging.error("Error unisolating endpoint: %s", error)
        return {}

def get_endpoint_quarantine_status(endpoint_id: str) -> dict:
    """
    Retrieves the quarantine status for a specific endpoint from the Cortex XDR API.

    Args:
    endpoint_id: The ID of the endpoint to retrieve the quarantine status for.

    Returns:
    Dictionary containing the quarantine status for the endpoint.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/endpoints/quarantine-status"

    # Define the request body
    request_body = {
        "request_data": {
            "endpoint_id": endpoint_id
        }
    }

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.post(
            endpoint_url, headers=auth_headers, json=request_body, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the quarantine status for the endpoint
        return response_json["reply"]

    except requests.exceptions.RequestException as error:
        logging.error("Error getting endpoint quarantine status: %s", error)
        return {}

def quarantine_endpoint(endpoint_id: str) -> dict:
    """
    Quarantines an endpoint from the Cortex XDR API.

    Args:
    endpoint_id: The ID of the endpoint to quarantine.

    Returns:
    Dictionary containing the response from the Cortex XDR API.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/endpoints/quarantine"

    # Define the request body
    request_body = {
        "request_data": {
            "endpoint_id": endpoint_id
        }
    }

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.post(
            endpoint_url, headers=auth_headers, json=request_body, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the response from the Cortex XDR API
        return response_json

    except requests.exceptions.RequestException as error:
        logging.error("Error quarantining endpoint: %s", error)
        return {}

def unquarantine_endpoint(endpoint_id: str) -> dict:
    """
    Unquarantines an endpoint from the Cortex XDR API.

    Args:
    endpoint_id: The ID of the endpoint to unquarantine.

    Returns:
    Dictionary containing the response from the Cortex XDR API.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/endpoints/unquarantine"

    # Define the request body
    request_body = {
        "request_data": {
            "endpoint_id": endpoint_id
        }
    }

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.post(
            endpoint_url, headers=auth_headers, json=request_body, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the response from the Cortex XDR API
        return response_json

    except requests.exceptions.RequestException as error:
        logging.error("Error unquarantining endpoint: %s", error)
        return {}

def get_endpoint_network_details(endpoint_id: str) -> dict:
    """
    Retrieves network details for a specific endpoint from the Cortex XDR API.

    Args:
    endpoint_id: The ID of the endpoint to retrieve network details for.

    Returns:
    Dictionary containing the network details for the endpoint.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/endpoints/network"

    # Define the request body
    request_body = {
        "request_data": {
            "endpoint_id": endpoint_id
        }
    }

    try:
        # Send the API request with a timeout of 10 seconds
        response = requests.post(
            endpoint_url, headers=auth_headers, json=request_body, timeout=10
        )
        response.raise_for_status()  # Raise an exception if the response status code is not 200

        # Parse the response JSON
        response_json = json.loads(response.text)

        # Return the network details for the endpoint
        return response_json["reply"]

    except requests.exceptions.RequestException as error:
        logging.error("Error getting endpoint network details: %s", error)
        return {}
