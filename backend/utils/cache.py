from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class SimpleCache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() < entry["expires"]:
                return entry["value"]
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        self.cache[key] = {
            "value": value,
            "expires": datetime.now() + timedelta(seconds=self.ttl)
        }

    def clear(self) -> None:
        self.cache.clear()

    def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]

cache = SimpleCache()
