"""
This file contains the R7_ISVM_Auth class for handling authentication with the InsightVM API.
"""
import os
import logging
import base64
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Set up logging
logging.basicConfig(filename='api_r7_auth.log', level=logging.INFO)

class R7_ISVM_Auth:
    """
    A class for handling authentication with the InsightVM API.

    Attributes:
        isvm_api_username (str): The InsightVM API username.
        isvm_api_password (str): The InsightVM API password.
        isvm_base_url (str): The InsightVM API base URL.
    """

    def __init__(self) -> None:
        """
        Initializes the R7Auth class by loading the necessary environment variables and checking for missing credentials.
        """
        self.isvm_api_username = os.environ.get('INSIGHTVM_API_USERNAME')
        self.isvm_api_password = os.environ.get('INSIGHTVM_API_PASSWORD')
        self.isvm_base_url = os.environ.get('INSIGHTVM_BASE_URL')

        if not self.isvm_api_username or not self.isvm_api_password or not self.isvm_base_url:
            logging.error("Missing ISVM API credentials or BASE URL. Please check .env file.")
            raise ValueError("Missing ISVM API credentials or BASE URL. Please check .env file.")

    def get_isvm_encoded_auth_header(self) -> dict[str, str]:
        """
        Returns the Authorization header with the Base64 encoded hash of the username and password.

        Returns:
            A dictionary containing the Authorization header.
        """
        auth_string = f"{self.isvm_api_username}:{self.isvm_api_password}"
        encoded_auth_string = base64.b64encode(auth_string.encode()).decode()
        auth_headers = {"Authorization": f"Basic {encoded_auth_string}"}
        return auth_headers
