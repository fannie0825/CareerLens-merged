#!/usr/bin/env python3
"""
Test Azure OpenAI Endpoint using secrets.toml configuration
============================================================
This script reads from .streamlit/secrets.toml and tests connectivity.

Usage:
    python3 tests/test_endpoint_from_secrets.py
"""

import sys
import os
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

import requests


def load_secrets():
    """Load secrets from .streamlit/secrets.toml"""
    secrets_path = Path(__file__).parent.parent / '.streamlit' / 'secrets.toml'
    
    if not secrets_path.exists():
        print(f"❌ secrets.toml not found at: {secrets_path}")
        print("\nCreate .streamlit/secrets.toml with:")
        print("""
AZURE_OPENAI_ENDPOINT = "https://hkust.azure-api.net/openai"
AZURE_OPENAI_API_KEY = "your-key-here"
AZURE_OPENAI_DEPLOYMENT = "gpt-4o-mini"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
""")
        return None
    
    secrets = {}
    with open(secrets_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                secrets[key] = value
    
    return secrets


def test_deployment(endpoint, api_key, deployment, api_version="2024-02-15-preview"):
    """Test a specific deployment."""
    # Clean endpoint
    endpoint = endpoint.rstrip('/')
    if endpoint.endswith('/openai'):
        endpoint = endpoint[:-7]
    
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": "Say 'hello' only"}],
        "max_tokens": 10
    }
    
    print(f"\n🔗 Testing: {deployment}")
    print(f"   URL: {url[:80]}...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"   ✅ SUCCESS! Response: '{content}'")
            return True
            
        elif response.status_code == 404:
            try:
                error = response.json().get('error', {}).get('message', response.text[:200])
            except:
                error = response.text[:200]
            print(f"   ❌ 404 Not Found")
            print(f"      Error: {error[:100]}")
            return False
            
        elif response.status_code == 401:
            print(f"   ❌ 401 Unauthorized - Invalid API key")
            return False
            
        elif response.status_code == 403:
            print(f"   ⚠️ 403 Forbidden - No access to this deployment")
            return False
            
        elif response.status_code == 429:
            print(f"   ⚠️ 429 Rate Limited - But connection works!")
            return True
            
        else:
            print(f"   ⚠️ {response.status_code}: {response.text[:100]}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️ Timeout")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def main():
    print("=" * 60)
    print(" Azure OpenAI Endpoint Test (from secrets.toml)")
    print("=" * 60)
    
    secrets = load_secrets()
    if not secrets:
        return 1
    
    endpoint = secrets.get('AZURE_OPENAI_ENDPOINT')
    api_key = secrets.get('AZURE_OPENAI_API_KEY')
    deployment = secrets.get('AZURE_OPENAI_DEPLOYMENT', 'gpt-4o-mini')
    embedding_deployment = secrets.get('AZURE_OPENAI_EMBEDDING_DEPLOYMENT', 'text-embedding-3-small')
    api_version = secrets.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
    
    if not endpoint or not api_key:
        print("❌ Missing AZURE_OPENAI_ENDPOINT or AZURE_OPENAI_API_KEY in secrets.toml")
        return 1
    
    print(f"\n📍 Endpoint: {endpoint}")
    print(f"🔑 API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else '***'}")
    print(f"📦 Deployment: {deployment}")
    print(f"📦 Embedding Deployment: {embedding_deployment}")
    print(f"📌 API Version: {api_version}")
    
    # Test the configured deployment
    print("\n" + "-" * 60)
    print("Testing configured deployment...")
    print("-" * 60)
    
    success = test_deployment(endpoint, api_key, deployment, api_version)
    
    if not success:
        # Try alternative deployments
        print("\n" + "-" * 60)
        print("Trying alternative deployment names...")
        print("-" * 60)
        
        alternatives = [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4",
            "gpt-35-turbo",
            "gpt-3.5-turbo",
            "chatgpt",
        ]
        
        # Remove the one we already tried
        alternatives = [d for d in alternatives if d != deployment]
        
        for alt in alternatives:
            if test_deployment(endpoint, api_key, alt, api_version):
                print(f"\n✅ Found working deployment: {alt}")
                print(f"\nUpdate your secrets.toml:")
                print(f'AZURE_OPENAI_DEPLOYMENT = "{alt}"')
                return 0
        
        print("\n" + "=" * 60)
        print("❌ No working deployment found!")
        print("=" * 60)
        print("""
Possible causes:
1. The deployment name is different - contact HKUST IT
2. API key doesn't have access to any models
3. The endpoint URL is incorrect

Try contacting HKUST IT support for:
- Available deployment names
- Correct endpoint URL format
""")
        return 1
    
    print("\n" + "=" * 60)
    print("✅ Configuration is working!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
