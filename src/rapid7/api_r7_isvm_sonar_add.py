import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

def load_csv(filepath):
    # Load CSV and return as DataFrame, automatically stripping whitespace from headers
    return pd.read_csv(filepath, skipinitialspace=True)

def create_sonar_query(url, name, criteria, username, password):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "name": name,
        "criteria": criteria
    }
    response = requests.post(url, auth=HTTPBasicAuth(username, password), headers=headers, json=payload)
    return response.status_code, response.text

def main():
    filepath = 'path_to_your_file.csv'  # Update with your file path
    url = 'https://localhost:3780/api/3/sonar_queries'  # API endpoint
    username = 'your_username'
    password = 'your_password'
    
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
        
        status_code, response_text = create_sonar_query(url, name, criteria, username, password)
        
        print("Status Code:", status_code)
        print("Response:", response_text)

if __name__ == '__main__':
    main()
