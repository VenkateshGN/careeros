import os
from typing import Optional
# Mock redis import for now since we don't have the dependency installed in requirements yet
# import redis

class CacheService:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/2")
        # self.client = redis.Redis.from_url(self.redis_url)
        self._mock_store = {}

    def get(self, key: str) -> Optional[str]:
        # return self.client.get(key)
        print(f"Mock Cache Get Data for: {key}")
        return self._mock_store.get(key)

    def set(self, key: str, value: str, expire: int = 3600):
        # self.client.set(key, value, ex=expire)
        print(f"Mock Cache Set Data for: {key}")
        self._mock_store[key] = value

cache = CacheService()
