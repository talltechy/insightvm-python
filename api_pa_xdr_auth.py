import os
from datetime import datetime, timezone
import secrets
import string
import hashlib
from typing import Optional
from dotenv import load_dotenv

# Python script that uses the Palo Alto Cortex XDR API and Rapid7 InsightVM API
# This script is provided as-is without warranty of any kind.
# Palo Alto Networks and Rapid7 do not support this script.
# Use at your own risk.
# Written by Matt Wyen (https://github.com/talltechy)

# https://cortex-panw.stoplight.io/docs/cortex-xdr/3u3j0e7hcx8t1-get-started-with-cortex-xdr-ap-is

# Load environment variables from .env file
load_dotenv('.env')

# Get required credentials from environment variables
xdr_api_key = os.getenv('XDR_API_KEY')
xdr_api_key_id = os.getenv('XDR_API_KEY_ID')

if not xdr_api_key or not xdr_api_key_id:
    raise ValueError("Missing XDR API credentials. Please check .env file.")

def generate_advanced_authentication(api_key: str, api_key_id: str,
                                      payload: Optional[dict] = None):
    """
    Generates advanced authentication headers for Cortex XDR API requests.

    Args:
    api_key: The XDR API key.
    api_key_id: The XDR API key ID.
    payload: Optional dictionary containing the request payload.

    Returns:
    Dictionary containing the authentication headers.
    """
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
    auth_string = (api_key + nonce + timestamp_str).encode('utf-8')
    auth_key = hashlib.sha256(auth_string).hexdigest()
    headers = {
        'Authorization': auth_key,
        'x-xdr-nonce': nonce,
        'x-xdr-timestamp': timestamp_str,
        'x-xdr-auth-id': str(api_key_id)
    }
    return headers
