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
    level=logging.DEBUG # Change the logging level to DEBUG
)

# Define the endpoint for retrieving assets from the InsightVM API
ASSETS_ENDPOINT = '/api/3/assets'

# Define the maximum number of assets to retrieve per page
PAGE_SIZE = 50

def get_all_assets():
    """
    Retrieves all assets from the InsightVM API and returns them as a list of dictionaries.
    """
    # Get the ISVM API credentials and base URL from environment variables
    _, _, isvm_base_url = load_r7_isvm_api_credentials()

    # Define the headers for the API request
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': get_isvm_basic_auth_header()
    }

    # Define the parameters for the API request
    params = {
        'size': PAGE_SIZE,
        'page': 0
    }

    # Initialize the list of assets
    assets = []

    # Loop through all pages of assets
    while True:
        # Make the API request
        response = requests.get(isvm_base_url + ASSETS_ENDPOINT, headers=headers, params=params)

        # Check if the API request was successful
        if response.status_code != 200:
            logging.error('Failed to retrieve assets from the InsightVM API: %s', response.text)
            break

        # Parse the API response
        data = json.loads(response.text)

        # Add the assets from the current page to the list
        assets.extend(data['assets'])

        # Check if there are more pages of assets
        if data['pagination']['next_page'] is None:
            break

        # Update the parameters for the next page of assets
        params['page'] = data['pagination']['next_page']

    return assets

def create_assets_table(conn):
    """
    Creates the assets table in the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assets (
            id TEXT PRIMARY KEY,
            hostname TEXT,
            ip_address TEXT,
            mac_address TEXT,
            fqdn TEXT,
            netbios_name TEXT,
            operating_system TEXT,
            last_assessed TEXT
        )
    ''')
    conn.commit()

def insert_assets(conn, assets):
    """
    Inserts the specified assets into the assets table in the SQLite database.
    """
    cursor = conn.cursor()
    for asset in assets:
        cursor.execute('''
            INSERT OR REPLACE INTO assets (
                id,
                hostname,
                ip_address,
                mac_address,
                fqdn,
                netbios_name,
                operating_system,
                last_assessed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            asset['id'],
            asset['host_name'],
            asset['ip_address'],
            asset['mac_address'],
            asset['fqdn'],
            asset['netbios_name'],
            asset['operating_system'],
            asset['last_assessed']
        ))
    conn.commit()

def main():
    """
    Retrieves all assets from the InsightVM API and stores them in a SQLite database.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('assets.db')

    # Create the assets table if it doesn't exist
    create_assets_table(conn)

    # Retrieve all assets from the InsightVM API
    assets = get_all_assets()

    # Insert the assets into the SQLite database
    insert_assets(conn, assets)

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    main()

