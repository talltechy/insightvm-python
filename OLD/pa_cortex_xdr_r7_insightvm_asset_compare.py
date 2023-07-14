import base64
import json
import requests
from dotenv import load_dotenv
from src.paloalto.cortex_xdr.api_pa_xdr_auth import generate_advanced_authentication, load_xdr_api_credentials
from src.rapid7.api_r7_auth import load_r7_isvm_api_credentials, get_isvm_api_headers
from src.paloalto.cortex_xdr.api_pa_xdr import get_endpoints, get_endpoint_details
from src.rapid7.api_r7_isvm import search_isvm_endpoint

# Load environment variables from .env file
load_dotenv(".env")

# Load the XDR API credentials
xdr_api_key, xdr_api_key_id, xdr_base_url = load_xdr_api_credentials()

# Load the InsightVM API credentials
(
    isvm_api_username,
    isvm_api_password,
    isvm_base_url,
) = load_r7_isvm_api_credentials()

# Load the ISVM API headers
isvm_headers = get_isvm_api_headers()

# Check if there is any credentials missing
if not xdr_api_key or not xdr_api_key_id or not xdr_base_url:
    raise ValueError("Missing XDR API credentials. Please check .env file.")

if not isvm_api_username or not isvm_api_password or not isvm_base_url:
    raise ValueError("Missing InsightVM API credentials. Please check .env file.")

# Get assets from Cortex XDR


# Search for a endpoint in InsightVM
def search_isvm_endpoint(base_url, headers, hostname, verify=False):
    """
    Search for a hostname in the InsightVM API.

    :param base_url: Base URL for the InsightVM API
    :param headers: Headers for the InsightVM API request
    :param hostname: Hostname to search for
    :return: Matching assets (list of dictionaries)
    """
    url = f"{base_url}/api/3/assets/search"
    body = {
        "match": "all",
        "filters": [{"field": "host-name", "operator": "is", "value": hostname}],
    }
    response = requests.post(url, headers=headers, json=body, timeout=10)

    if response.status_code != 200:
        print(f"Error searching for hostname {hostname} in InsightVM")
        return None

    data = response.json()
    return data.get("resources", [])


# Check if assets from Cortex XDR are also in InsightVM
for asset in xdr_assets:
    hostname = asset.get("hostname")
    if hostname:
        matching_assets = search_isvm_endpoint(isvm_base_url, isvm_headers, hostname)

        if matching_assets:
            logger.info(f"{hostname} found in InsightVM")
        else:
            logger.info(f"{hostname} not found in InsightVM")
    else:
        logger.info("Hostname not found in Cortex XDR asset")
