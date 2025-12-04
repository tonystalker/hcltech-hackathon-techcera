import urllib.request
import json
import time

BASE_URL = "http://localhost:8000"

def register():
    url = f"{BASE_URL}/auth/register"
    data = {
        "name": "Delete Test",
        "email": "deletetest@example.com",
        "password": "password123",
        "role": "patient"
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Register status: {response.status}")
            return True
    except urllib.error.HTTPError as e:
        print(f"Register failed: {e.code} {e.read().decode()}")
        return False

def login():
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": "deletetest@example.com",
        "password": "password123"
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode())
            print(f"Login status: {response.status}")
            return response_data["access_token"]
    except urllib.error.HTTPError as e:
        print(f"Login failed: {e.code} {e.read().decode()}")
        return None

def delete_account(token):
    url = f"{BASE_URL}/users/me"
    req = urllib.request.Request(
        url,
        method="DELETE",
        headers={'Authorization': f'Bearer {token}'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Delete status: {response.status}")
            return True
    except urllib.error.HTTPError as e:
        print(f"Delete failed: {e.code} {e.read().decode()}")
        return False

def verify_deleted():
    print("Verifying account is deleted by trying to login...")
    token = login()
    if token:
        print("FAIL: Still able to login after deletion")
        return False
    else:
        print("SUCCESS: Unable to login after deletion")
        return True

def main():
    # Wait for server to start
    print("Waiting for server...")
    time.sleep(5)
    
    print("Step 1: Register")
    if not register():
        # Maybe already exists, try login
        print("User might already exist, proceeding to login")
    
    print("Step 2: Login")
    token = login()
    if not token:
        print("Could not login, aborting")
        return

    print("Step 3: Delete Account")
    if delete_account(token):
        print("Step 4: Verify Deletion")
        verify_deleted()

if __name__ == "__main__":
    main()
