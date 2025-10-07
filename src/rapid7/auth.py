"""
Unified authentication module for Rapid7 InsightVM and Platform APIs.

This module provides clean, modern authentication classes that use
the requests library's built-in HTTPBasicAuth for secure credential handling.
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(filename='rapid7_auth.log', level=logging.ERROR)


class InsightVMAuth:
    """
    Authentication handler for InsightVM API.
    
    This class manages InsightVM API credentials and provides an
    HTTPBasicAuth object for use with the requests library.
    
    Attributes:
        username (str): The InsightVM API username.
        password (str): The InsightVM API password.
        base_url (str): The InsightVM API base URL.
        auth (HTTPBasicAuth): Requests HTTPBasicAuth object.
    
    Example:
        >>> auth = InsightVMAuth()
        >>> response = requests.get(url, auth=auth.auth)
        
        >>> # Or with explicit credentials:
        >>> auth = InsightVMAuth(
        ...     username="user",
        ...     password="pass",
        ...     base_url="https://insightvm.example.com"
        ... )
    """
    
    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize InsightVM authentication.
        
        Args:
            username: InsightVM API username (optional, reads from env if not provided)
            password: InsightVM API password (optional, reads from env if not provided)
            base_url: InsightVM base URL (optional, reads from env if not provided)
        
        Raises:
            ValueError: If required credentials are missing.
        """
        self.username = username or os.getenv('INSIGHTVM_API_USERNAME')
        self.password = password or os.getenv('INSIGHTVM_API_PASSWORD')
        self.base_url = base_url or os.getenv('INSIGHTVM_BASE_URL')
        
        if not all([self.username, self.password, self.base_url]):
            logging.error("Missing InsightVM API credentials or base URL")
            raise ValueError(
                "Missing InsightVM API credentials. Required: "
                "INSIGHTVM_API_USERNAME, INSIGHTVM_API_PASSWORD, INSIGHTVM_BASE_URL"
            )
        
        # Create HTTPBasicAuth object
        self.auth = HTTPBasicAuth(self.username, self.password)
    
    def __repr__(self):
        return f"InsightVMAuth(base_url='{self.base_url}')"


class PlatformAuth:
    """
    Authentication handler for Rapid7 Insight Platform API.
    
    This class manages Platform API credentials and provides
    headers for API requests.
    
    Attributes:
        api_key (str): The Platform API key.
        base_url (str): The Platform API base URL.
    
    Example:
        >>> auth = PlatformAuth()
        >>> headers = auth.get_headers()
        >>> response = requests.get(url, headers=headers)
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize Platform API authentication.
        
        Args:
            api_key: Platform API key (optional, reads from env if not provided)
            base_url: Platform base URL (optional, reads from env if not provided)
        
        Raises:
            ValueError: If required credentials are missing.
        """
        self.api_key = api_key or os.getenv('INSIGHT_PLATFORM_API_KEY')
        self.base_url = base_url or os.getenv('INSIGHT_PLATFORM_BASE_URL')
        
        if not all([self.api_key, self.base_url]):
            logging.error("Missing Platform API credentials or base URL")
            raise ValueError(
                "Missing Platform API credentials. Required: "
                "INSIGHT_PLATFORM_API_KEY, INSIGHT_PLATFORM_BASE_URL"
            )
    
    def get_headers(self) -> dict:
        """
        Get headers for Platform API requests.
        
        Returns:
            Dictionary containing required headers.
        """
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }
    
    def __repr__(self):
        return f"PlatformAuth(base_url='{self.base_url}')"
