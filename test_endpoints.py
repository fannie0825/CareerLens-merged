import os
import pytest
import requests
import json

# This file is a live endpoint diagnostic (not a unit test).
# It is disabled by default to avoid accidental network calls in CI/local runs.
if os.getenv("RUN_LIVE_ENDPOINT_TESTS") != "1":
    pytest.skip(
        "Live endpoint diagnostics are disabled by default. Set RUN_LIVE_ENDPOINT_TESTS=1 to enable.",
        allow_module_level=True,
    )

API_KEY = "90fa7411f0e542d59bec8dca4c51fa7c"
API_VERSION = "2024-02-15-preview"
DEPLOYMENTS = ["gpt-4o-mini", "gpt-4o", "gpt-35-turbo"]

# Base URLs to test
BASES = [
    "https://hkust.azure-api.net/openai",
    "https://hkust.azure-api.net"
]

def test_chat_completion(base_url, deployment):
    # Construct full URL manually to be sure
    # Standard pattern: {base}/deployments/{deployment}/chat/completions?api-version={version}
    # Note: If base ends in /openai, we use it. If not, we might need to add it or not depending on APIM.
    
    # Clean base
    base = base_url.rstrip('/')
    
    # Pattern 1: {base}/deployments/... (Assuming /openai is already in base or not needed)
    url1 = f"{base}/deployments/{deployment}/chat/completions?api-version={API_VERSION}"
    
    # Pattern 2: {base}/openai/deployments/... (Standard Azure pattern if base is just hostname)
    url2 = f"{base}/openai/deployments/{deployment}/chat/completions?api-version={API_VERSION}"

    urls_to_test = [url1]
    if "/openai" not in base:
        urls_to_test.append(url2)

    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 5
    }

    for url in urls_to_test:
        print(f"Testing URL: {url}")
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ SUCCESS!")
                print(f"Response: {response.json()['choices'][0]['message']['content']}")
                return True
            else:
                try:
                    print(f"Error: {response.json().get('error', {}).get('message', response.text)}")
                except:
                    print(f"Error: {response.text[:100]}")
        except Exception as e:
            print(f"Exception: {e}")
        print("-" * 20)
    return False

def main():
    print(f"API Key: {API_KEY[:5]}...{API_KEY[-4:]}")
    
    found_success = False
    for base in BASES:
        for dep in DEPLOYMENTS:
            if test_chat_completion(base, dep):
                found_success = True
                print(f"\n🎉 FOUND WORKING CONFIGURATION:")
                print(f"Base URL: {base}")
                print(f"Deployment: {dep}")
                break
        if found_success:
            break
            
    if not found_success:
        print("\n❌ All combinations failed.")

if __name__ == "__main__":
    main()
