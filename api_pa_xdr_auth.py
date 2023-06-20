import os
from datetime import datetime, timezone
import secrets
import hashlib
from typing import Optional
from dotenv import load_dotenv

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
    nonce = secrets.token_urlsafe(64)

    # Generate timestamp string
    timestamp_ms = int(datetime.now(timezone.utc).timestamp()) * 1000
    timestamp_str = f"{timestamp_ms}"

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

# Call the `generate_advanced_authentication()` function
auth_headers = generate_advanced_authentication(xdr_api_key, xdr_api_key_id)
print(auth_headers)
