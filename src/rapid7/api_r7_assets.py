"""
This module provides functions for retrieving and storing assets from the InsightVM API.
"""
import logging
import sqlite3
from dotenv import load_dotenv
from .api_r7_isvm import get_assets_isvm
from .api_r7_auth import load_r7_isvm_api_credentials, get_isvm_access_token
# Load environment variables from .env file
load_dotenv(".env")

# Load the R7 ISVM API credentials
isvm_api_username, isvm_api_password, isvm_base_url = load_r7_isvm_api_credentials()

# Set up logging
logging.basicConfig(filename='api_r7_isvm.log', level=logging.ERROR)

def store_assets_in_database():
    """
    Retrieve assets from the InsightVM API and store them in a local SQLite database.
    """

    # Connect to the local SQLite database
    conn = sqlite3.connect('isvm_assets.db')
    cursor = conn.cursor()

    # Create the assets table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS assets
                    (id text, hostname text, os text, last_seen text)''')

    try:
        # Get the assets from the InsightVM API
        assets = get_assets_isvm(isvm_base_url, {}, verify=False)

        if assets is not None:
            # Insert the assets into the database
            for asset in assets.get('resources', []):
                asset_id = asset.get('id')
                hostname = asset.get('host-name')
                os_type = asset.get('os')
                last_seen = asset.get('last-scan-time')

                cursor.execute(
                    "INSERT INTO assets VALUES (?, ?, ?, ?)",
                    (asset_id, hostname, os_type, last_seen)
                )

            # Commit the changes and close the connection
            conn.commit()

    except sqlite3.Error as error:
        # Handle the error and print an error message
        print(f"An error occurred: {str(error)}")

    finally:
        # Close the connection
        conn.close()
