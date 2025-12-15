import os
import requests
import json

# --- 1. FILL IN YOUR REAL CREDENTIALS HERE FOR TESTING ---
# (Do not commit this file to GitHub with real keys!)
ENDPOINT = "https://hkust.azure-api.net/openai"
API_KEY = "90fa7411f0e542d59bec8dca4c51fa7c"
DEPLOYMENT_NAME = "gpt-4o-mini"
API_VERSION = "2024-02-15-preview"

# --- 2. CONSTRUCT THE FULL URL ---
# The HKUST wrapper usually looks like:
# https://hkust.azure-api.net/openai/deployments/{deployment-id}/chat/completions?api-version={api-version}
full_url = f"{ENDPOINT}/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version={API_VERSION}"

print(f"Testing URL: {full_url}")

# --- 3. PREPARE THE PAYLOAD ---
headers = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

data = {
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Test connection. Say hello!"}
    ],
    "max_tokens": 50
}

# --- 4. SEND THE REQUEST ---
try:
    response = requests.post(full_url, headers=headers, json=data)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS! Connection established.")
        print("Response:", response.json()['choices'][0]['message']['content'])
    elif response.status_code == 404:
        print("❌ ERROR 404: Resource Not Found.")
        print("Possible causes:")
        print("1. The Deployment Name is wrong (is it really 'gpt-4o-mini'?).")
        print("2. The Endpoint URL format is wrong (does it need '/openai'?).")
    elif response.status_code == 401:
        print("❌ ERROR 401: Unauthorized.")
        print("Possible causes:")
        print("1. Your API Key is incorrect.")
    else:
        print(f"❌ ERROR: {response.text}")

except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
