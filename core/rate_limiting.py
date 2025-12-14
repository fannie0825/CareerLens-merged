"""
Single source of truth for rate limiting and token tracking.

This module provides thread-safe implementations of:
- TokenUsageTracker: Track API token usage and calculate costs
- RateLimiter: Rate limiting for API calls
"""

from datetime import datetime, timedelta
from collections import defaultdict
import threading


class TokenUsageTracker:
    """Track API token usage across the application.
    
    Thread-safe tracker for monitoring token consumption and calculating
    costs across different API services (embeddings, completions).
    
    Attributes:
        usage: Dictionary tracking prompt and completion tokens per model
        embedding_tokens: Total embedding tokens used
        cost_usd: Running total of estimated costs in USD
    """
    
    # Pricing constants (per 1000 tokens)
    EMBEDDING_COST_PER_1K = 0.00002  # text-embedding-3-small
    GPT4_MINI_PROMPT_COST_PER_1K = 0.00015
    GPT4_MINI_COMPLETION_COST_PER_1K = 0.0006
    
    def __init__(self):
        self.usage = defaultdict(lambda: {"prompt": 0, "completion": 0})
        self.lock = threading.Lock()
        
        # Detailed tracking
        self.total_tokens = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_embedding_tokens = 0
        self.cost_usd = 0.0
    
    def add_usage(self, model: str, prompt_tokens: int, completion_tokens: int):
        """Add token usage for a specific model.
        
        Args:
            model: The model name/identifier
            prompt_tokens: Number of prompt tokens used
            completion_tokens: Number of completion tokens used
        """
        with self.lock:
            self.usage[model]["prompt"] += prompt_tokens
            self.usage[model]["completion"] += completion_tokens
            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            self.total_tokens += prompt_tokens + completion_tokens
            
            # Calculate cost based on model
            if "embedding" in model.lower():
                self.cost_usd += ((prompt_tokens + completion_tokens) / 1000) * self.EMBEDDING_COST_PER_1K
            else:
                self.cost_usd += (prompt_tokens / 1000) * self.GPT4_MINI_PROMPT_COST_PER_1K
                self.cost_usd += (completion_tokens / 1000) * self.GPT4_MINI_COMPLETION_COST_PER_1K
    
    def add_embedding_tokens(self, tokens: int):
        """Track embedding token usage.
        
        Args:
            tokens: Number of embedding tokens used
        """
        with self.lock:
            self.total_embedding_tokens += tokens
            self.total_tokens += tokens
            self.cost_usd += (tokens / 1000) * self.EMBEDDING_COST_PER_1K
    
    def add_completion_tokens(self, prompt_tokens: int, completion_tokens: int):
        """Track completion token usage.
        
        Args:
            prompt_tokens: Number of prompt tokens used
            completion_tokens: Number of completion tokens used
        """
        with self.lock:
            self.total_prompt_tokens += prompt_tokens
            self.total_completion_tokens += completion_tokens
            self.total_tokens += prompt_tokens + completion_tokens
            self.cost_usd += (prompt_tokens / 1000) * self.GPT4_MINI_PROMPT_COST_PER_1K
            self.cost_usd += (completion_tokens / 1000) * self.GPT4_MINI_COMPLETION_COST_PER_1K
    
    def get_total_cost(self) -> float:
        """Calculate total cost across all tracked usage.
        
        Returns:
            Total estimated cost in USD
        """
        with self.lock:
            return round(self.cost_usd, 6)
    
    def get_summary(self) -> dict:
        """Get comprehensive usage summary.
        
        Returns:
            Dictionary containing token counts and estimated costs
        """
        with self.lock:
            return {
                'total_tokens': self.total_tokens,
                'embedding_tokens': self.total_embedding_tokens,
                'prompt_tokens': self.total_prompt_tokens,
                'completion_tokens': self.total_completion_tokens,
                'estimated_cost_usd': round(self.cost_usd, 4),
                'usage_by_model': dict(self.usage)
            }
    
    def reset(self):
        """Reset all counters to zero."""
        with self.lock:
            self.usage.clear()
            self.total_tokens = 0
            self.total_prompt_tokens = 0
            self.total_completion_tokens = 0
            self.total_embedding_tokens = 0
            self.cost_usd = 0.0


class RateLimiter:
    """Rate limiting for API calls.
    
    Thread-safe rate limiter that enforces a maximum number of calls
    within a sliding time window.
    
    Args:
        max_calls: Maximum number of calls allowed in the time window
        time_window: Time window in seconds (default: 60 for per-minute limiting)
    
    Example:
        limiter = RateLimiter(max_calls=10, time_window=60)
        if limiter.allow_request():
            # Make API call
            pass
        else:
            # Handle rate limit exceeded
            pass
    """
    
    def __init__(self, max_calls: int, time_window: int = 60):
        self.max_calls = max_calls
        self.time_window = timedelta(seconds=time_window)
        self.calls = []
        self.lock = threading.Lock()
    
    def allow_request(self) -> bool:
        """Check if a request is allowed under the rate limit.
        
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        with self.lock:
            now = datetime.now()
            # Remove old calls outside the time window
            self.calls = [t for t in self.calls if now - t < self.time_window]
            
            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return True
            return False
    
    def wait_if_needed(self):
        """Wait if rate limit is exceeded, then record the request.
        
        This method blocks until a request slot is available.
        Compatible with the existing RateLimiter interface used in api_clients.py.
        """
        import time
        
        if self.max_calls <= 0:
            return
        
        with self.lock:
            now = datetime.now()
            # Remove old calls outside the time window
            self.calls = [t for t in self.calls if now - t < self.time_window]
            
            if len(self.calls) >= self.max_calls:
                # Calculate wait time until oldest call expires
                oldest_call = min(self.calls)
                wait_seconds = (self.time_window - (now - oldest_call)).total_seconds() + 0.1
                
                if wait_seconds > 0:
                    # Release lock during sleep
                    self.lock.release()
                    try:
                        time.sleep(wait_seconds)
                    finally:
                        self.lock.acquire()
                    
                    # Refresh the calls list after waiting
                    now = datetime.now()
                    self.calls = [t for t in self.calls if now - t < self.time_window]
            
            self.calls.append(datetime.now())
    
    def get_remaining_calls(self) -> int:
        """Get the number of remaining calls allowed in current window.
        
        Returns:
            Number of calls remaining before rate limit is hit
        """
        with self.lock:
            now = datetime.now()
            self.calls = [t for t in self.calls if now - t < self.time_window]
            return max(0, self.max_calls - len(self.calls))
    
    def get_reset_time(self) -> float:
        """Get seconds until the rate limit window resets.
        
        Returns:
            Seconds until oldest call expires from the window,
            or 0 if no calls are tracked
        """
        with self.lock:
            now = datetime.now()
            self.calls = [t for t in self.calls if now - t < self.time_window]
            
            if not self.calls:
                return 0.0
            
            oldest_call = min(self.calls)
            reset_time = (self.time_window - (now - oldest_call)).total_seconds()
            return max(0.0, reset_time)
