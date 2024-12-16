import json
import time
import jwt
import requests

async def getAccessToken():
    try:
        with open("gcpkey.json", 'r') as f:
            service_account = json.load(f)

        now = int(time.time())
        expiry = now + 3600  # Token expires in 1 hour

        payload = {
            "iss": service_account["client_email"],
            "scope": "https://www.googleapis.com/auth/devstorage.read_only",  # Read-only scope
            "aud": "https://oauth2.googleapis.com/token",
            "exp": expiry,
            "iat": now
        }

        token = jwt.encode(payload, service_account["private_key"], algorithm='RS256')

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': token
        }

        response = requests.post('https://oauth2.googleapis.com/token', headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for bad status codes

        access_token = response.json().get('access_token')
        return access_token

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None