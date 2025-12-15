import os
import sys
from openai import AzureOpenAI

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
# We try to load from .streamlit/secrets.toml first.
# If that fails, you can manually set these variables.
# -----------------------------------------------------------------------------

API_KEY = "your-azure-openai-api-key"
ENDPOINT = "https://hkust.azure-api.net/openai"
API_VERSION = "2024-02-15-preview"

# Attempt to load from secrets.toml
try:
    import toml
    if os.path.exists(".streamlit/secrets.toml"):
        print("Loading credentials from .streamlit/secrets.toml...")
        with open(".streamlit/secrets.toml", "r") as f:
            secrets = toml.load(f)
            API_KEY = secrets.get("AZURE_OPENAI_API_KEY", API_KEY)
            ENDPOINT = secrets.get("AZURE_OPENAI_ENDPOINT", ENDPOINT)
            API_VERSION = secrets.get("AZURE_OPENAI_API_VERSION", API_VERSION)
except ImportError:
    print("toml module not found, using hardcoded variables.")
except Exception as e:
    print(f"Error loading secrets.toml: {e}")

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

    # Check for placeholder values
    if "your-" in API_KEY or "your-" in ENDPOINT:
        print("\n⚠️  WARNING: It looks like you are using placeholder credentials.")
        print("   Please update .streamlit/secrets.toml or edit this script with your actual keys.")
    
    print("\nAttempting to initialize AzureOpenAI client...")
    
    try:
        # Handle cleanup of endpoint if needed (SDK handles it mostly, but good to be safe)
        # The SDK expects the base endpoint, usually without /openai/deployments/... 
        # but often with /openai for APIM. 
        # We will use it exactly as provided first.
        
        client = AzureOpenAI(
            api_key=API_KEY,
            api_version=API_VERSION,
            azure_endpoint=ENDPOINT
        )
        
        print("Client initialized. Calling client.models.list()...")
        
        # This is the "List Models" call
        response = client.models.list()
        
        print("\n✅ SUCCESS! Connection established.")
        print(f"Found {len(response.data)} models/deployments:\n")
        
        for model in response.data:
            print(f"  • ID: {model.id}")
            # print(f"    Object: {model.object}")
            # print(f"    Created: {model.created}")
            
        print("\n--- INSTRUCTIONS ---")
        print("1. Find the ID in the list above that corresponds to GPT-4 or GPT-4o.")
        print("2. Copy that EXACT ID.")
        print("3. Paste it into .streamlit/secrets.toml as:")
        print("   AZURE_OPENAI_DEPLOYMENT = \"your-copied-id\"")
        
    except Exception as e:
        print("\n❌ CONNECTION FAILED")
        print(f"Error details: {str(e)}")
        
        if "404" in str(e):
            print("\nAnalysis: 404 Not Found.")
            print("If this is the 'List Models' endpoint failing, your AZURE_OPENAI_ENDPOINT is likely incorrect.")
            print("Try removing '/openai' from the end, or verify the URL in Azure Portal.")
        elif "401" in str(e):
            print("\nAnalysis: 401 Unauthorized.")
            print("Your AZURE_OPENAI_API_KEY is incorrect.")

if __name__ == "__main__":
    debug_azure_connection()
