import requests
import json
import base64
import os
import string
import secrets
from datetime import datetime, timezone
import hashlib
from typing import Optional
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Python script that uses the Palo Alto Cortex XDR API and Rapid7 InsightVM API
# This script is provided as-is without warranty of any kind.
# Palo Alto Networks and Rapid7 do not support this script.
# Use at your own risk.
# Written by Matt Wyen (https://github.com/talltechy)

# Get required credentials from environment variables
xdr_api_key = os.getenv('XDR_API_KEY')
xdr_api_key_id = os.getenv('XDR_API_KEY_ID')
xdr_base_url = os.getenv('XDR_BASE_URL')

# Get InsightVM API credentials from environment variables
insightvm_api_username = os.getenv('INSIGHTVM_API_USERNAME')
insightvm_api_password = os.getenv('INSIGHTVM_API_PASSWORD')
insightvm_base_url = os.getenv('INSIGHTVM_BASE_URL')

# Check for missing credentials and raise an error if any is missing
if not xdr_api_key or not xdr_api_key_id or not xdr_base_url:
    raise ValueError("Missing XDR API credentials. Please check .env file.")

if not insightvm_api_username or not insightvm_api_password or not insightvm_base_url:
    raise ValueError("Missing InsightVM API credentials. Please check .env file.")

def xdr_advanced_authentication(xdr_api_key: str, xdr_api_key_id: str,
                                      payload: Optional[dict] = None):
    # Use empty dictionary as payload if payload is None
    payload = payload or {}

    # Generate nonce value
    nonce_length = 64
    nonce_chars = string.ascii_letters + string.digits
    nonce = ''.join(secrets.choice(nonce_chars) for _ in range(nonce_length))

    # Generate timestamp string
    timestamp_ms = int(datetime.now(timezone.utc).timestamp()) * 1000
    timestamp_str = str(timestamp_ms)

    # Generate authentication headers
    auth_string = (xdr_api_key + nonce + timestamp_str).encode('utf-8')
    auth_key = hashlib.sha256(auth_string).hexdigest()
    headers = {
        'Authorization': auth_key,
        'x-xdr-nonce': nonce,
        'x-xdr-timestamp': timestamp_str,
        'x-xdr-auth-id': str(xdr_api_key_id)
    }
    return headers

# Set up request headers
xdr_headers = xdr_advanced_authentication(xdr_api_key, xdr_api_key_id)

insightvm_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Basic " + base64.b64encode(f"{insightvm_api_username}:{insightvm_api_password}".encode("utf-8")).decode("utf-8")
}

# Get assets from Cortex XDR
xdr_url = f"{xdr_base_url}/public_api/v1/endpoints/get_endpoints/"
xdr_response = requests.post(xdr_url, headers=xdr_headers)

if xdr_response.status_code != 200:
    print("Error getting assets from Cortex XDR")
    exit()

xdr_data = json.loads(xdr_response.text)
xdr_assets = xdr_data["reply"]["endpoints"]

# Get assets from InsightVM
insightvm_url = f"{insightvm_base_url}/api/3/assets"
insightvm_response = requests.get(insightvm_url, headers=insightvm_headers)

if insightvm_response.status_code != 200:
    print("Error getting assets from InsightVM")
    exit()

insightvm_data = json.loads(insightvm_response.text)
insightvm_assets = insightvm_data["resources"]

# Check if assets from Cortex XDR are also in InsightVM
for xdr_asset in xdr_assets:
    if xdr_asset["hostname"] in [insightvm_asset["host-name"] for insightvm_asset in insightvm_assets]:
        print(f"{xdr_asset['hostname']} found in InsightVM")
    else:
        print(f"{xdr_asset['hostname']} not found in InsightVM")
