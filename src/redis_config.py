import os

import redis


class RedisClient:
    def __init__(self):
        self.client = redis.StrictRedis(
            host=os.environ.get("REDIS_HOST", 'localhost'),
            port=int(os.environ.get("REDIS_PORT", 6379)),
            db=int(os.environ.get("REDIS_DB", 0)),
        )

    def set_key(self, key, value, expire=None):
        self.client.set(key, value, ex=expire)

    def get_key(self, key):
        return self.client.get(key)

    def delete_key(self, key):
        self.client.delete(key)


redis_client = RedisClient()