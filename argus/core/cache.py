"""Session-only response cache; nothing is written to disk."""
import time
TTL = 86400
_cache = {}
def get(url):
    item = _cache.get(url)
    return item[1] if item and time.time() - item[0] <= TTL else None
def put(url, content):
    _cache[url] = (time.time(), content)
