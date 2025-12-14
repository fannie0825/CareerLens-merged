"""
Azure OpenAI service clients.
"""
from openai import AzureOpenAI
from config import Config
from core.rate_limiting import TokenUsageTracker, RateLimiter


class AzureOpenAIClient:
    """Base Azure OpenAI client."""
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
        )
        self.token_tracker = TokenUsageTracker()
        self.rate_limiter = RateLimiter(max_calls=60, time_window=60)


class EmbeddingGenerator(AzureOpenAIClient):
    """Generate embeddings using Azure OpenAI."""
    def generate(self, text: str, model: str = None):
        model = model or Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT
        
        if not self.rate_limiter.allow_request():
            raise Exception("Rate limit exceeded")
        
        response = self.client.embeddings.create(
            input=text,
            model=model
        )
        
        self.token_tracker.add_usage(
            model=model,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=0
        )
        
        return response.data[0].embedding


class TextGenerator(AzureOpenAIClient):
    """Generate text using Azure OpenAI."""
    def generate(self, prompt: str, model: str = None, **kwargs):
        model = model or Config.AZURE_OPENAI_DEPLOYMENT
        
        if not self.rate_limiter.allow_request():
            raise Exception("Rate limit exceeded")
        
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        
        self.token_tracker.add_usage(
            model=model,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens
        )
        
        return response.choices[0].message.content
