"""This module contains functions to return user-friendly messages based on status codes."""
def create_sonar_query_sm(status_code, response):
    """Return a user-friendly message based on the status code for a Sonar Query."""
    if status_code == 200:
        return f"Sonar Query created successfully. ID: {response.json()['id']}"
    elif status_code == 400:
        return f"Bad Request: {response.json()['message']}"
    elif status_code == 401:
        return f"Unauthorized: {response.json()['message']}"
    elif status_code == 500:
        return f"Internal Server Error: {response.json()['message']}"
    elif status_code == 503:
        return f"Service Unavailable: {response.json()['message']}"
    else:
        return response.text
