import base64
import hashlib
import json
import logging
import os
import secrets
import string
import sys
from datetime import datetime, timezone
from typing import Optional

import requests
from dotenv import find_dotenv, load_dotenv
from requests.exceptions import Timeout

from logger import setup_logging

# Get the directory the script is in
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the log file path to be in the script directory
log_file_path = os.path.join(script_dir, 'myapp.log')

# Setup logging with the log file path
setup_logging(log_file_path)

# Create a logger instance
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

# Load environment variables
xdr_api_key = os.getenv('XDR_API_KEY')
xdr_api_key_id = os.getenv('XDR_API_KEY_ID')
xdr_base_url = os.getenv('XDR_BASE_URL')

insightvm_api_username = os.getenv('INSIGHTVM_API_USERNAME')
insightvm_api_password = os.getenv('INSIGHTVM_API_PASSWORD')
insightvm_base_url = os.getenv('INSIGHTVM_BASE_URL')

# Check if there is any credential missing
if not xdr_api_key or not xdr_api_key_id or not xdr_base_url:
    raise ValueError("Missing XDR API credentials. Please check .env file.")

if not insightvm_api_username or not insightvm_api_password or not insightvm_base_url:
    raise ValueError("Missing InsightVM API credentials. Please check .env file.")


def xdr_advanced_authentication(xdr_api_key: str, xdr_api_key_id: str,
                                 payload: Optional[dict] = None):
    """
    Generate Cortex XDR advanced authentication headers.

    :param xdr_api_key: API Key string
    :param xdr_api_key_id: API Key ID string
    :param payload: If not None, attach more data to the request.
    :return: Generated headers (dictionary)
    """
    payload = payload or {}
    nonce_length = 64
    nonce_chars = string.ascii_letters + string.digits
    nonce = ''.join(secrets.choice(nonce_chars) for _ in range(nonce_length))

    timestamp_ms = int(datetime.now(timezone.utc).timestamp()) * 1000
    timestamp_str = str(timestamp_ms)

    auth_string = (xdr_api_key + nonce + timestamp_str).encode('utf-8')
    auth_key = hashlib.sha256(auth_string).hexdigest()
    headers = {
        'Authorization': auth_key,
        'x-xdr-nonce': nonce,
        'x-xdr-timestamp': timestamp_str,
        'x-xdr-auth-id': str(xdr_api_key_id)
    }
    headers.update(payload)
    return headers


xdr_headers = xdr_advanced_authentication(xdr_api_key, xdr_api_key_id)

insightvm_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Basic " + base64.b64encode(f"{insightvm_api_username}:{insightvm_api_password}"
                                                  .encode("utf-8")).decode("utf-8")
}


# Check if base_url are reachable with timeout
def check_base_url(base_url, headers, timeout=5, verify=True):
    """
    Check if the given base_url is reachable.
    """
    try:
        response = requests.head(base_url, headers=headers, timeout=timeout, verify=verify)
    except (requests.exceptions.RequestException, Timeout) as e:
        print(f"Error connecting to {base_url}: {e}")
        sys.exit(1)

    return f"Connected to {base_url} with status code {response.status_code}"

# Then, when calling the function, you can provide the `verify` parameter value
logger.info(check_base_url(xdr_base_url, xdr_headers, verify=True))
logger.info(check_base_url(insightvm_base_url, insightvm_headers, verify=False))

# Get assets from Cortex XDR
xdr_url = f"{xdr_base_url}/public_api/v1/endpoints/get_endpoints/"
xdr_response = requests.post(xdr_url, headers=xdr_headers)

if xdr_response.status_code != 200:
    logger.error("Error getting assets from Cortex XDR")
    exit()

xdr_data = json.loads(xdr_response.text)
xdr_assets = xdr_data.get("reply", [])  # Use get() method to avoid the code stop running if "reply" key is not found

# Function to search for a hostname in InsightVM
def search_insightvm_hostname(base_url, headers, hostname, verify=False):
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
        "filters": [
            {
                "field": "host-name",
                "operator": "is",
                "value": hostname
            }
        ]
    }
    response = requests.post(url, headers=headers, json=body)

    if response.status_code != 200:
        logger.error(f"Error searching for hostname {hostname} in InsightVM")
        return None

    data = json.loads(response.text)
    return data.get("resources", [])


# Check if assets from Cortex XDR are also in InsightVM
for asset in xdr_assets:
    hostname = asset.get("hostname")
    if hostname:
        matching_assets = search_insightvm_hostname(insightvm_base_url, insightvm_headers, hostname)

        if matching_assets:
            logger.info(f"{hostname} found in InsightVM")
        else:
            logger.info(f"{hostname} not found in InsightVM")
    else:
        logger.info("Hostname not found in Cortex XDR asset")
