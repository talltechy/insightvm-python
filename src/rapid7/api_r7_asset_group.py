"""
This module provides functions to interact with the Rapid7 InsightVM API to create asset groups.
"""

import logging
import urllib3
from dotenv import load_dotenv
import requests
from src.rapid7.api_r7_auth import load_r7_isvm_api_credentials, get_isvm_basic_auth_header

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(filename='api_r7_asset_group.log', level=logging.ERROR)

def create_high_risk_asset_group():
    """
    Creates a dynamic asset group based on criteria and prints out the ID with a URL.
    """
    urllib3.disable_warnings()
    # Get the ISVM API credentials and base URL from environment variables
    _, _, isvm_base_url = load_r7_isvm_api_credentials()
    auth_headers = get_isvm_basic_auth_header()
    url = f"{isvm_base_url}/api/3/asset_groups"
    headers = {
        "Content-Type": "application/json",
        **auth_headers,
    }
    payload = {
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
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            verify=False,
            timeout=90
        ).json()
        ag_id = response["id"]
        print(
            f"Asset Group {ag_id} created and can be found at {isvm_base_url}/group.jsp?groupid={ag_id}"
        )
    except requests.exceptions.RequestException as error:
        logging.exception("Error creating asset group: %s", error)
        raise
