"""
This module retrieves assets from the Rapid7 InsightVM API and stores them in a SQLite database.
"""

import json
import sqlite3
import logging
import requests
from api_r7_auth import load_r7_isvm_api_credentials, get_isvm_basic_auth_header

logging.basicConfig(
    filename='api_r7_isvm_get_assets.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def create_database():
    """
    Create a new SQLite database and table to store the assets.
    """
    try:
        conn = sqlite3.connect('assets.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS assets
                     (id INTEGER PRIMARY KEY,
                     hostname TEXT,
                     ip_address TEXT,
                     os TEXT,
                     last_scan_date TEXT)''')
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        logging.error("Failed to create database.")
        logging.error(error)
        raise

def insert_assets(assets):
    """
    Insert the assets into the SQLite database.
    """
    try:
        conn = sqlite3.connect('assets.db')
        cursor = conn.cursor()

        # Loop through each asset and insert it into the database
        for asset in assets:
            cursor.execute(
                "INSERT INTO assets (id, hostname, ip_address, os, last_scan_date) VALUES (?, ?, ?, ?, ?)",
                (
                    asset['id'],
                    asset['host_name'],
                    asset['ip_address'],
                    asset['os'],
                    asset['last_scan_date']
                )
            )

        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        logging.error("Failed to insert assets into the database.")
        logging.error(error)
        raise

def get_assets():
    """
    Retrieve the assets from the Rapid7 InsightVM API.
    """
    try:
        # Get the ISVM API credentials and base URL from environment variables
        _, _, isvm_base_url = load_r7_isvm_api_credentials()

        # Construct the URL for the assets endpoint
        assets_url = (
            f"{isvm_base_url}/api/3/assets"
            "?limit=50"
        )

        # Set up the request headers
        headers = get_isvm_basic_auth_header()

        # Make a GET request to the assets endpoint to retrieve all assets
        response = requests.get(
            assets_url,
            headers=headers,
            timeout=10, # Add a timeout argument to avoid hanging indefinitely
            verify=False # Ignore SSL errors for testing purposes
        )

        # Check if the request was successful
        if response.status_code != 200:
            logging.error("Failed to retrieve assets.")
            raise ValueError("Failed to retrieve assets.")

        # Parse the JSON response
        assets = json.loads(response.content)

        # Insert the assets into the database
        insert_assets(assets)
        logging.info("Assets retrieved and inserted into the database.")
    except requests.RequestException as error:
        logging.error("Failed to retrieve assets from the API.")
        logging.error(error)
        raise

# Call the create_database function to create a new database and table
create_database()

# Call the get_assets function to retrieve the assets and insert them into the database
get_assets()
