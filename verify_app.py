#!/usr/bin/env python3
import requests
import time

base_url = 'http://127.0.0.1:5017' # Use the port the server will run on

def verify_endpoint(url, expected_status=200, method='GET', data=None):
    try:
        if method == 'GET':
            response = requests.get(url, timeout=10)
        elif method == 'POST':
            response = requests.post(url, data=data, timeout=10)
        else:
            print(f"Unsupported method: {method}")
            return False

        print(f"URL: {url}")
        print(f"Method: {method}")
        print(f"Status Code: {response.status_code}")
        print(f"Content Snippet: {response.text[:200]}...")
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
        return True
    except requests.exceptions.ConnectionError:
        print(f"Connection Error: Could not connect to {url}. Is the server running?")
    except requests.exceptions.Timeout:
        print(f"Timeout Error: Request to {url} timed out.")
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {e}")
    return False

print("Starting Flask application verification...")

# Verify root route
print("
Verifying root route (should be 'Hello, World!')")
verify_endpoint(base_url + '/')

# Verify new proposal form route
print("
Verifying new proposal form route")
verify_endpoint(base_url + '/proposals/new')

# Verify proposals list route (requires database connection)
print("
Verifying proposals list route (requires database connection)")
verify_endpoint(base_url + '/proposals')

# Verify edit proposal form route (assuming proposal with ID 1 exists)
print("
Verifying edit proposal form route for ID 1")
verify_endpoint(base_url + '/proposals/1/edit')

print("
Verification complete.")
