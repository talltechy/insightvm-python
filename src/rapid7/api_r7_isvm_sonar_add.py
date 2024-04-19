"""This script demonstrates how to create a Sonar Query in InsightVM using the API."""

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values

secrets = dotenv_values(".env")

def load_csv(filepath):
    """
        DataFrame: The loaded data.
    Returns:

        filepath (str): The path to the CSV file.
    Args:

    Load a CSV file and return it as a DataFrame, automatically stripping whitespace from headers.
    """
    return pd.read_csv(filepath, skipinitialspace=True)

def create_sonar_query(url, name, criteria, username, password):
    """Send a POST request to create a Sonar Query.

    Args:
        url (str): The API endpoint.
        name (str): The name of the Sonar Query.
        criteria (dict): The criteria for the Sonar Query.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        tuple: The status code and response text from the API.
    """
    headers = {'Content-Type': 'application/json'}
    payload = {
        "name": name,
        "criteria": criteria
    }
    response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, json=payload, timeout=10)
    return response.status_code, response.text

def main():
    """
    Main function to create Sonar queries based on data from a CSV file.

    This function reads data from a CSV file, cleans the data, and creates Sonar queries based on the data.
    The queries are then sent to the specified InsightVM host using the provided credentials.

    Parameters:
        None

    Returns:
        None
    """
    filepath = 'test.csv'  # Update with your file path
    ivm_host = secrets['ivm_host']
    ivm_port = secrets['ivm_port']
    username = secrets['ivm_username']
    password = secrets['ivm_password']
    # Construct the URL using the host and port
    url = f'https://{ivm_host}:{ivm_port}/api/3/sonar_queries'  # API endpoint

    # Load data
    df = load_csv(filepath)

    # Clean data by stripping any leading/trailing whitespace from string data
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Loop over rows in DataFrame
    for _, row in df.iterrows():
        filters = []

        # Create domain filter if domain is present
        if 'domain' in df.columns and pd.notna(row['domain']):
            filters.append({
                "type": "domain-contains",
                "domain": row['domain']
            })

        # Create IP range filter if IP range is present
        if 'ip_lower' in df.columns and 'ip_upper' in df.columns and pd.notna(row['ip_lower']) and pd.notna(row['ip_upper']):
            filters.append({
                "type": "ip-address-range",
                "lower": row['ip_lower'],
                "upper": row['ip_upper']
            })

        # Skip this row if no filters were created
        if not filters:
            continue

        # Prompt for days
        days = input("Enter the number of days for 'scan-date-within-the-last' (default 30): ").strip()
        days = int(days) if days.isdigit() else 30
        filters.append({
            "type": "scan-date-within-the-last",
            "days": days
        })

        criteria = {"filters": filters}
        name = "Example Sonar Query"
        name = row['domain'] if pd.notna(row['domain']) else row['ip_lower'] if pd.notna(row['ip_lower']) else f"{row['ip_lower']} - {row['ip_upper']}"
        status_code, response_text = create_sonar_query(url, name, criteria, username, password)
        print("Status Code:", status_code)
        print("Response:", response_text)

if __name__ == '__main__':
    main()
