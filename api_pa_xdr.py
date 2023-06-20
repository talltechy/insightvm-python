import json
from typing import Optional
import requests
from dotenv import load_dotenv
from api_pa_xdr_auth import generate_advanced_authentication

# Load environment variables from .env file
load_dotenv('.env')

# Call the function to generate the authentication headers
auth_headers = generate_advanced_authentication(xdr_api_key, xdr_api_key_id)

# Define the base URL for the Cortex XDR API
BASE_URL = 'https://api.paloaltonetworks.com/xdr/v2'

def get_incidents(auth_headers: dict, query: Optional[str] = None):
    """
    Retrieves a list of incidents from the Cortex XDR API.

    Args:
    auth_headers: Dictionary containing the authentication headers.
    query: Optional string containing the query to filter the incidents.

    Returns:
    List of incidents.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/incidents"

    # Define the query parameters
    params = {}
    if query:
        params['query'] = query

    # Send the API request with a timeout of 10 seconds
    response = requests.get(endpoint_url, headers=auth_headers, params=params, timeout=10)

    # Parse the response JSON
    response_json = json.loads(response.text)

    # Return the list of incidents
    return response_json['reply']

def get_endpoints(auth_headers: dict, query: Optional[str] = None):
    """
    Retrieves a list of endpoints from the Cortex XDR API.

    Args:
    auth_headers: Dictionary containing the authentication headers.
    query: Optional string containing the query to filter the endpoints.

    Returns:
    List of endpoints.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/endpoints"

    # Define the query parameters
    params = {}
    if query:
        params['query'] = query

    # Send the API request with a timeout of 10 seconds
    response = requests.get(endpoint_url, headers=auth_headers, params=params, timeout=10)

    # Parse the response JSON
    response_json = json.loads(response.text)

    # Return the list of endpoints
    return response_json['reply']

def get_alerts(auth_headers: dict, query: Optional[str] = None):
    """
    Retrieves a list of alerts from the Cortex XDR API.

    Args:
    auth_headers: Dictionary containing the authentication headers.
    query: Optional string containing the query to filter the alerts.

    Returns:
    List of alerts.
    """
    # Define the endpoint URL
    endpoint_url = f"{BASE_URL}/alerts"

    # Define the query parameters
    params = {}
    if query:
        params['query'] = query

    # Send the API request with a timeout of 10 seconds
    response = requests.get(endpoint_url, headers=auth_headers, params=params, timeout=10)

    # Parse the response JSON
    response_json = json.loads(response.text)

    # Return the list of alerts
    return response_json['reply']
