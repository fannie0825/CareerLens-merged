import requests

API_KEY = "90fa7411f0e542d59bec8dca4c51fa7c"
API_VERSION = "2024-02-01"  # Confirmed working
ENDPOINT = "https://hkust.azure-api.net/openai"

DEPLOYMENTS = [
    "text-embedding-3-small",
    "text-embedding-ada-002",
    "embedding",
    "embeddings",
    "ada"
]

def test_embedding(deployment):
    url = f"{ENDPOINT}/deployments/{deployment}/embeddings?api-version={API_VERSION}"
    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "input": "test",
        "model": deployment
    }
    
    print(f"Testing: {deployment}")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ SUCCESS! Found embedding deployment: {deployment}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    return False

if __name__ == "__main__":
    for d in DEPLOYMENTS:
        if test_embedding(d):
            break
