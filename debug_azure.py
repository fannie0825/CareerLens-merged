import os
import sys
from openai import AzureOpenAI

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------

API_KEY = "90fa7411f0e542d59bec8dca4c51fa7c"
ENDPOINT = "https://hkust.azure-api.net"  # Trying base without /openai first, as SDK might add it
API_VERSION = "2024-02-15-preview"

# -----------------------------------------------------------------------------
# MAIN SCRIPT
# -----------------------------------------------------------------------------

def debug_azure_connection():
    print(f"\n--- Azure OpenAI Connection Test (List Models) ---\n")
    print(f"Endpoint:    {ENDPOINT}")
    print(f"API Version: {API_VERSION}")
    
    # Mask key for display
    masked_key = f"{API_KEY[:5]}...{API_KEY[-4:]}" if len(API_KEY) > 10 else "***"
    print(f"API Key:     {masked_key}")

    print("\nAttempting to initialize AzureOpenAI client...")
    
    try:
        # Client 1: Base endpoint (standard)
        print("\n1. Testing with base endpoint: https://hkust.azure-api.net")
        client = AzureOpenAI(
            api_key=API_KEY,
            api_version=API_VERSION,
            azure_endpoint="https://hkust.azure-api.net"
        )
        try:
            response = client.models.list()
            print("✅ SUCCESS! (Base endpoint)")
            for model in response.data:
                print(f"  • ID: {model.id}")
            return
        except Exception as e:
            print(f"  Failed: {e}")

        # Client 2: With /openai suffix
        print("\n2. Testing with /openai endpoint: https://hkust.azure-api.net/openai")
        client = AzureOpenAI(
            api_key=API_KEY,
            api_version=API_VERSION,
            azure_endpoint="https://hkust.azure-api.net/openai"
        )
        try:
            response = client.models.list()
            print("✅ SUCCESS! (/openai endpoint)")
            for model in response.data:
                print(f"  • ID: {model.id}")
            return
        except Exception as e:
            print(f"  Failed: {e}")
            
    except Exception as e:
        print(f"\n❌ CRITICAL FAILURE: {str(e)}")

if __name__ == "__main__":
    debug_azure_connection()
