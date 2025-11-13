import redis
import json
from typing import Optional, Any
from app.config import settings

class CacheManager:
    def __init__(self):
        self.enabled = not settings.DEMO_MODE
        if self.enabled:
            try:
                self.client = redis.from_url(settings.REDIS_URL, decode_responses=True)
                self.client.ping()
            except Exception as e:
                print(f"Redis connection failed: {e}, falling back to no-cache mode")
                self.enabled = False

    def get(self, key: str) -> Optional[Any]:
        if not self.enabled:
            return None
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except Exception:
            return None

    def set(self, key: str, value: Any, ttl: int = None):
        if not self.enabled:
            return
        try:
            ttl = ttl or settings.CACHE_TTL
            self.client.setex(key, ttl, json.dumps(value))
        except Exception:
            pass

cache = CacheManager()
