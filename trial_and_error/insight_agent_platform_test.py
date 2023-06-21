"""
This module retrieves assets from the InsightVM platform API.
"""

import os
from requests.structures import CaseInsensitiveDict
import requests

# Load the API key and base URL from environment variables
api_key = os.getenv('INSIGHT_PLATFORM_API_KEY')
base_url = os.getenv('INSIGHT_PLATFORM_BASE_URL')

# Set the API endpoint for retrieving assets
endpoint = f"{base_url}/idr/v1/assets/_search"

# Set the headers for the API request
headers = CaseInsensitiveDict({
    'X-Api-Key': api_key,
    'Content-Type': 'application/json'
})

# Set the query parameters for the API request
params = {
    'q': 'os:Windows'
}

# Send the API request
response = requests.get(endpoint, headers=headers, params=params, timeout=10)

# Check if the request was successful
if response.status_code == 200:
    # Print the response body
    print(response.json())
else:
    # Print the error message
    print(f"Error: {response.status_code} - {response.text}")
