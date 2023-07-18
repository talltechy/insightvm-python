import os
import logging
import base64
import json
import urllib3
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(filename='api_r7_auth.log', level=logging.ERROR)

def load_r7_isvm_api_credentials(isvm_api_username=None, isvm_api_password=None, isvm_base_url=None):
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
        logging.error("Missing ISVM API credentials or BASE URL. Please check .env file.")
        raise ValueError("Missing ISVM API credentials or BASE URL. Please check .env file.")

    return isvm_api_username, isvm_api_password, isvm_base_url

def get_isvm_basic_auth_header() -> dict:
    """
    Returns the Authorization header with the Base64 encoded hash of the username and password.

    Returns:
        A dictionary containing the Authorization header.
    """
    isvm_api_username, isvm_api_password, _ = load_r7_isvm_api_credentials()
    auth_headers = {}
    auth_string = f"{isvm_api_username}:{isvm_api_password}"
    encoded_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
    auth_headers = {"Authorization": f"Basic {encoded_auth_string}"}
    return auth_headers

def create_ag():
    """creates a dynamic asset group based off criteria and prints out the id with a url."""
    urllib3.disable_warnings()
    # Get the ISVM API credentials and base URL from environment variables
    _, _, isvm_base_url = load_r7_isvm_api_credentials()
    auth_headers = get_isvm_basic_auth_header()
    url = f"https://{isvm_base_url}:3780/api/3/asset_groups"
    headers = {
        "Content-Type": "application/json",
        **auth_headers,
    }
    payload = json.dumps(
        {
            "description": "Assets with unacceptable high risk required immediate remediation.",
            "name": "High Risk Assets",
            "searchCriteria": {
                "filters": [
                    {
                        "field": "risk-score",
                        "lower": "",
                        "operator": "is-greater-than",
                        "upper": "",
                        "value": 25000,
                        "values": ["string"],
                    }
                ],
                "match": "all",
            },
            "type": "dynamic",
            "vulnerabilities": {},
        }
    )
    response = requests.post(
        url,
        headers=headers,
        data=payload,
        verify=False,
        timeout=90
    ).json()
    agid = response["id"]
    print(
        f"Asset Group {agid} created and can be found at https://{isvm_base_url}:3780/group.jsp?groupid={agid}"
    )
    return
