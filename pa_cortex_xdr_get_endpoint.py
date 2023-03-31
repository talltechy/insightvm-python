import os
import requests
from datetime import datetime, timezone
import secrets
import string
import hashlib
from dotenv import load_dotenv
from api_functions import get_xdr_credentials

load_dotenv()  # loads environment variables from ".env" file

def generate_advanced_authentication(xdr_api_key, xdr_api_key_id, xdr_base_url):
    nonce = "".join([secrets.choice(string.ascii_letters + string.digits) for _ in range(64)])
    timestamp = str(int(datetime.now(timezone.utc).timestamp()) * 1000) 
    auth_key = "{}{}{}".format(xdr_api_key, nonce, timestamp).encode("utf-8")
    xdr_api_key_hash = hashlib.sha256(auth_key).hexdigest()
    headers = {
        "x-xdr-timestamp": timestamp,
        "x-xdr-nonce": nonce,
        "x-xdr-auth-id": str(xdr_api_key_id),
        "Authorization": xdr_api_key_hash
    }
    payload = {
        'request_data': {
            'limit': 10
        }
    }
    res = requests.post(url=f"{xdr_base_url}/public_api/v1/endpoints/get_endpoint/",
                        headers=headers,
                        json=payload)
    return res

API_KEY, API_ID, BASE_URL = get_xdr_credentials()
response = generate_advanced_authentication(API_KEY, API_ID, BASE_URL)

if response.ok:
    endpoints = response.json()['reply']['endpoints']
    for i, endpoint in enumerate(endpoints, start=1):
        print(f"Endpoint {i}:")
        print(f"  Endpoint ID: {endpoint['endpoint_id']}")
        print(f"  Hostname: {endpoint['endpoint_name']}")
        print(f"  OS Type: {endpoint['os_type']}")
        print(f"  IP: {endpoint['ip']}")
else:
    print(f"Error: Unable to fetch endpoints. Status code: {response.status_code}")
