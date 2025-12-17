import os
import requests
import json

# --- HKUST SPECIFIC CONFIGURATION ---
# Hardcoded for testing certainty
API_KEY = "90fa7411f0e542d59bec8dca4c51fa7c"

# 1. The Base Endpoint from the docs (curl command)
BASE_URL = "https://hkust.azure-api.net"

# 2. The Deployment Name explicitly listed in the 'Supported Models' table
DEPLOYMENT_NAME = "gpt-4o-mini"

# 3. The API Version explicitly used in the 'API Key Verification' curl command
API_VERSION = "2024-10-21"

def test_hkust_connection():
    print(f"--- Testing HKUST Connection ---")
    
    # Construct the URL exactly as shown in the HKUST curl example:
    # https://hkust.azure-api.net/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-10-21
    full_url = f"{BASE_URL}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"
    
    print(f"Target URL: {full_url}")
    
    # HKUST docs specify using the 'api-key' header
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Payload
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Test connection."}
        ]
    }

    try:
        response = requests.post(full_url, headers=headers, json=payload)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS! Connection established.")
            print("Response:", response.json()['choices'][0]['message']['content'])
        elif response.status_code == 404:
            print("ERROR 404: Resource Not Found.")
            print("Reasoning based on HKUST Docs:")
            print("1. Ensure your API Key is subscribed to the 'Azure OpenAI (personal)' product in the HKUST portal.")
            print("2. If you just subscribed, wait a few minutes for activation.")
        elif response.status_code == 401:
            print("ERROR 401: Unauthorized.")
            print("Check your API Key. Ensure you copied it from the 'Azure OpenAI (personal)' section.")
        elif response.status_code == 429:
             print("ERROR 429: Rate Limit Exceeded.")
             print("The docs state the limit is 60 requests per minute.")
        else:
            print(f"ERROR {response.status_code}")
            print("Raw Response:", response.text)
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    test_hkust_connection()
