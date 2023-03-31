import requests
import json
import base64
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Python script that uses the Cortex XDR API and the InsightVM API
# to check if assets in Cortex XDR are also found in InsightVM
# This script is provided as-is without warranty of any kind.
# Palo Alto Networks and Rapid7 do not support this script.
# Use at your own risk.
# Written by Matt Wyen (https://github.com/talltechy)

# Get Cortex XDR API credentials from environment variables
xdr_api_key = os.getenv('XDR_API_KEY')
xdr_api_secret = os.getenv('XDR_API_SECRET')
xdr_base_url = os.getenv('XDR_BASE_URL')

# Get InsightVM API credentials from environment variables
insightvm_api_key = os.getenv('INSIGHTVM_API_KEY')
insightvm_api_secret = os.getenv('INSIGHTVM_API_SECRET')
insightvm_base_url = os.getenv('INSIGHTVM_BASE_URL')

# Set up request headers
xdr_headers = {
    "x-xdr-auth-id": xdr_api_key,
    "x-xdr-auth-token": xdr_api_secret,
    "Content-Type": "application/json"
}

insightvm_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Basic " + base64.b64encode(f"{insightvm_api_key}:{insightvm_api_secret}".encode("utf-8")).decode("utf-8")
}

# Get assets from Cortex XDR
xdr_url = f"{xdr_base_url}/xdr/v2/endpoints/get_endpoints/"
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
