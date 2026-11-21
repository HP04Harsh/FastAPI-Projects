
import time
from typing import Any, Optional

# In-Memory Cache Store: { key: {"data": Any, "expiry": float} }
_cache_store = {}


def get_from_cache(key: str) -> Optional[Any]:
    """Retrieves item from cache if exists and not expired."""
    entry = _cache_store.get(key)
    if not entry:
        return None

    if time.time() > entry["expiry"]:
        # Cache expired
        del _cache_store[key]
        return None

    return entry["data"]


def set_to_cache(key: str, data: Any, ttl_seconds: int = 300) -> None:
    """Stores item in cache with TTL (seconds)."""
    _cache_store[key] = {
        "data": data,
        "expiry": time.time() + ttl_seconds
    }


def clear_cache() -> int:
    """Clears all cached items."""
    count = len(_cache_store)
    _cache_store.clear()
    return count


def get_cache_stats() -> dict:
    """Returns total items and active memory footprint statistics."""
    now = time.time()
    active_keys = [k for k, v in _cache_store.items() if v["expiry"] > now]
    return {
        "total_cached_entries": len(_cache_store),
        "active_valid_entries": len(active_keys)
    }