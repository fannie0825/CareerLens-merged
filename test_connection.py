import os
import sys
import toml
from openai import AzureOpenAI

# Mocking st.secrets if not running in Streamlit
class Secrets:
    def __init__(self):
        self._secrets = {}
        try:
            with open(".streamlit/secrets.toml", "r") as f:
                self._secrets = toml.load(f)
        except Exception as e:
            print(f"Error loading secrets: {e}")

    def __getitem__(self, key):
        return self._secrets[key]
    
    def get(self, key, default=None):
        return self._secrets.get(key, default)

# Check if running under streamlit (st.secrets would be available if we imported streamlit, but standalone is better)
try:
    import streamlit as st
    if not hasattr(st, "secrets") or not st.secrets:
        # Fallback if st.secrets is empty (e.g. running as script)
        secrets = Secrets()
    else:
        secrets = st.secrets
except ImportError:
    secrets = Secrets()

# Main logic
try:
    print(f"Loading secrets from: {secrets.get('AZURE_OPENAI_ENDPOINT', 'Not found')}")
    
    endpoint = secrets["AZURE_OPENAI_ENDPOINT"]
    
    client = AzureOpenAI(
        api_key=secrets["AZURE_OPENAI_API_KEY"],
        api_version=secrets["AZURE_OPENAI_API_VERSION"],
        azure_endpoint=endpoint
    )
    
    print("✅ Client initialized.")

    deployment = secrets["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]
    print(f"Testing embedding with deployment: {deployment}")
    
    response = client.embeddings.create(
        input="Test",
        model=deployment
    )
    print(f"✅ Connection successful! Embedding dimension: {len(response.data[0].embedding)}")

except Exception as e:
    print(f"❌ Error: {e}")
