import os
import requests
from datetime import datetime, timezone
import secrets
import string
import hashlib
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def get_xdr_credentials():
    xdr_api_key = os.getenv('XDR_API_KEY')
    xdr_api_key_id = os.getenv('XDR_API_KEY_ID')
    xdr_base_url = os.getenv('XDR_BASE_URL')
    return xdr_api_key, xdr_api_key_id, xdr_base_url

def generate_advanced_authentication(xdr_api_key_id, xdr_api_key, xdr_base_url):
    # Generate a 64 bytes random string
    nonce = "".join([secrets.choice(string.ascii_letters + string.digits) for _ in range(64)])
    # Get the current timestamp as milliseconds.
    timestamp = int(datetime.now(timezone.utc).timestamp()) * 1000
    # Generate the auth key:
    auth_key = "%s%s%s" % (xdr_api_key, nonce, timestamp)
    # Convert to bytes object
    auth_key = auth_key.encode("utf-8")
    # Calculate sha256:
    xdr_api_key_hash = hashlib.sha256(auth_key).hexdigest()
    # Generate HTTP call headers
    headers = {
        "x-xdr-timestamp": str(timestamp),
        "x-xdr-nonce": nonce,
        "x-xdr-auth-id": str(xdr_api_key_id),
        "Authorization": xdr_api_key_hash
    }

    # Define the request payload
    payload = {
        'request_data': {
            'limit': 10
        }
    }

    res = requests.post(url=f"{xdr_base_url}/public_api/v1/endpoints/get_endpoint/",
                        headers=headers,
                        json=payload)
    return res

# Get API credentials
API_KEY, API_ID, BASE_URL = get_xdr_credentials()

response = generate_advanced_authentication(API_ID, API_KEY, BASE_URL)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    endpoints = response.json()['reply']['endpoints']

    # Print endpoint information
    for i, endpoint in enumerate(endpoints, start=1):
        print(f"Endpoint {i}:")
        print(f"  Endpoint ID: {endpoint['endpoint_id']}")
        print(f"  Hostname: {endpoint['endpoint_name']}")
        print(f"  OS Type: {endpoint['os_type']}")
        print(f"  IP: {endpoint['ip']}")

else:
    print(f"Error: Unable to fetch endpoints. Status code: {response.status_code}")
