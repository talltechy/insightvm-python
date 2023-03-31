import requests
import json
import base64
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Python script that uses the Palo Alto Cortex XDR API and Rapid7 InsightVM API
# This script is provided as-is without warranty of any kind.
# Palo Alto Networks and Rapid7 do not support this script.
# Use at your own risk.
# Written by Matt Wyen (https://github.com/talltechy)

# Function to get Cortex XDR API credentials from environment variables:


def get_xdr_credentials():
    return os.getenv('XDR_API_KEY'), os.getenv('XDR_API_KEY_ID'), os.getenv('XDR_BASE_URL')

# Function to get InsightVM API credentials from environment variables:


def get_insightvm_credentials():
    insightvm_api_key = os.getenv('INSIGHTVM_API_KEY')
    insightvm_api_secret = os.getenv('INSIGHTVM_API_SECRET')
    insightvm_base_url = os.getenv('INSIGHTVM_BASE_URL')
    return insightvm_api_key, insightvm_api_secret, insightvm_base_url

# Function to set up XDR request headers:


def get_xdr_headers(api_key, api_secret):
    headers = {
        "x-xdr-auth-id": api_key,
        "x-xdr-auth-token": api_secret,
        "Content-Type": "application/json"
    }
    return headers

# Function to set up InsightVM request headers:


def get_insightvm_headers(api_key, api_secret):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode(f"{api_key}:{api_secret}".encode("utf-8")).decode("utf-8")
    }
    return headers
