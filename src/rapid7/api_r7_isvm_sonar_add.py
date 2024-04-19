"""This script demonstrates how to create a Sonar Query in InsightVM using the API."""

import ipaddress
import re
import pandas as pd
import requests
from dotenv import dotenv_values
from requests.auth import HTTPBasicAuth

secrets = dotenv_values(".env")

def load_csv(filepath):
    """
    Load a CSV file and return it as a DataFrame, automatically stripping whitespace from headers.
    """
    df = pd.read_csv(filepath, skipinitialspace=True)
    return df

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
    response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, json=payload, timeout=1, verify=False)
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

    # Verify that the CSV file has the correct format
    if 'target' not in df.columns:
        print("CSV file is not formatted correctly. It should have a 'target' column.")
        return

    # Add new columns for status code and response
    df['status_code'] = ''
    df['response'] = ''

    # Clean data by stripping any leading/trailing whitespace from string data
    df = df.apply(lambda x: x.map(str.strip) if x.dtype == "object" else x)

    # Prompt for days
    days = input("Enter the number of days for 'scan-date-within-the-last' (default 30): ").strip()
    days = int(days) if days.isdigit() else 30

    # Loop over rows in DataFrame
    for index, row in df.iterrows():
        filters = []
        target = row['target']

        # Check if target is a domain
        if re.match(r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}$', target):
            filters.append({
                "type": "domain-contains",
                "domain": target
            })
        else:
            try:
                # Check if target is an IP or IP range
                ip_range = ipaddress.ip_network(target, strict=False)
                filters.append({
                    "type": "ip-address-range",
                    "lower": str(ip_range.network_address),
                    "upper": str(ip_range.broadcast_address)
                })
            except ValueError:
                print(f"Invalid target: {target}")
                continue

        filters.append({
            "type": "scan-date-within-the-last",
            "days": days
        })

        criteria = {"filters": filters}
        name = "Example Sonar Query"
        name = target
        status_code, response_text = create_sonar_query(url, name, criteria, username, password)

        # Update status code and response in the DataFrame
        df.at[index, 'status_code'] = status_code
        df.at[index, 'response'] = response_text

    # Save the updated DataFrame to the CSV file
    df.to_csv(filepath, index=False)

    print("Status code and response added to the CSV file.")

if __name__ == '__main__':
    main()
