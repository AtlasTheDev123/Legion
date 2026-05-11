"""Caching layer for Legion Core Claw."""

import logging
import time
import hashlib
import json
from typing import Dict, Any, Optional, Union
from abc import ABC, abstractmethod
import threading
from collections import OrderedDict

logger = logging.getLogger(__name__)


class CacheEntry:
    """Cache entry with metadata."""

    def __init__(self, key: str, value: Any, ttl: Optional[int] = None):
        self.key = key
        self.value = value
        self.created_at = time.time()
        self.accessed_at = time.time()
        self.ttl = ttl
        self.access_count = 0

    def is_expired(self) -> bool:
        """Check if entry is expired."""
        if self.ttl is None:
            return False
        return time.time() - self.created_at > self.ttl

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "key": self.key,
            "value": self.value,
            "created_at": self.created_at,
            "accessed_at": self.accessed_at,
            "ttl": self.ttl,
            "access_count": self.access_count
        }


class CacheBackend(ABC):
    """Abstract base class for cache backends."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all cache entries."""
        pass

    @abstractmethod
    def has_key(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass


class MemoryCache(CacheBackend):
    """In-memory cache implementation."""

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.lock = threading.RLock()

    def _evict_if_needed(self) -> None:
        """Evict expired entries and enforce size limit."""
        # Remove expired entries
        expired_keys = [k for k, v in self.cache.items() if v.is_expired()]
        for key in expired_keys:
            del self.cache[key]

        # Enforce size limit (LRU eviction)
        while len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            self._evict_if_needed()
            if key in self.cache:
                entry = self.cache[key]
                entry.accessed_at = time.time()
                entry.access_count += 1
                self.cache.move_to_end(key)  # Mark as recently used
                return entry.value
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        with self.lock:
            self._evict_if_needed()
            entry = CacheEntry(key, value, ttl)
            self.cache[key] = entry
            self.cache.move_to_end(key)

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False

    def clear(self) -> None:
        """Clear all cache entries."""
        with self.lock:
            self.cache.clear()

    def has_key(self, key: str) -> bool:
        """Check if key exists in cache."""
        with self.lock:
            self._evict_if_needed()
            return key in self.cache

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_entries = len(self.cache)
            expired_entries = sum(1 for v in self.cache.values() if v.is_expired())
            total_accesses = sum(v.access_count for v in self.cache.values())

            return {
                "total_entries": total_entries,
                "expired_entries": expired_entries,
                "max_size": self.max_size,
                "total_accesses": total_accesses,
                "hit_rate": total_accesses / max(total_accesses, 1)  # Simplified
            }


class RedisCache(CacheBackend):
    """Redis cache implementation."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: Optional[str] = None):
        try:
            import redis
            self.redis = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
            self.redis.ping()  # Test connection
            self.available = True
        except ImportError:
            logger.warning("Redis not available, falling back to memory cache")
            self.available = False
            self.fallback_cache = MemoryCache()
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}, falling back to memory cache")
            self.available = False
            self.fallback_cache = MemoryCache()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.available:
            return self.fallback_cache.get(key)

        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        if not self.available:
            self.fallback_cache.set(key, value, ttl)
            return

        try:
            json_value = json.dumps(value)
            if ttl:
                self.redis.setex(key, ttl, json_value)
            else:
                self.redis.set(key, json_value)
        except Exception as e:
            logger.error(f"Redis set error: {e}")

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if not self.available:
            return self.fallback_cache.delete(key)

        try:
            return bool(self.redis.delete(key))
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False

    def clear(self) -> None:
        """Clear all cache entries."""
        if not self.available:
            self.fallback_cache.clear()
            return

        try:
            self.redis.flushdb()
        except Exception as e:
            logger.error(f"Redis clear error: {e}")

    def has_key(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self.available:
            return self.fallback_cache.has_key(key)

        try:
            return bool(self.redis.exists(key))
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False


class CacheManager:
    """Unified cache manager with multiple backends."""

    def __init__(self, default_backend: str = "memory", **backend_config):
        self.backends: Dict[str, CacheBackend] = {}
        self.default_backend = default_backend

        # Initialize backends
        self.backends["memory"] = MemoryCache(**backend_config.get("memory", {}))
        self.backends["redis"] = RedisCache(**backend_config.get("redis", {}))

        # Set default backend
        if default_backend not in self.backends:
            logger.warning(f"Backend '{default_backend}' not available, using memory")
            self.default_backend = "memory"

    def get_backend(self, backend_name: Optional[str] = None) -> CacheBackend:
        """Get cache backend."""
        backend_name = backend_name or self.default_backend
        return self.backends.get(backend_name, self.backends["memory"])

    def get(self, key: str, backend: Optional[str] = None) -> Optional[Any]:
        """Get value from cache."""
        return self.get_backend(backend).get(key)

    def set(self, key: str, value: Any, ttl: Optional[int] = None, backend: Optional[str] = None) -> None:
        """Set value in cache."""
        self.get_backend(backend).set(key, value, ttl)

    def delete(self, key: str, backend: Optional[str] = None) -> bool:
        """Delete value from cache."""
        return self.get_backend(backend).delete(key)

    def clear(self, backend: Optional[str] = None) -> None:
        """Clear cache."""
        self.get_backend(backend).clear()

    def has_key(self, key: str, backend: Optional[str] = None) -> bool:
        """Check if key exists."""
        return self.get_backend(backend).has_key(key)

    def get_stats(self, backend: Optional[str] = None) -> Dict[str, Any]:
        """Get cache statistics."""
        backend_instance = self.get_backend(backend)
        if hasattr(backend_instance, 'get_stats'):
            return backend_instance.get_stats()
        return {"backend": type(backend_instance).__name__}


class CachedFunction:
    """Decorator for caching function results."""

    def __init__(self, ttl: Optional[int] = None, backend: Optional[str] = None, key_func: Optional[callable] = None):
        self.ttl = ttl
        self.backend = backend
        self.key_func = key_func

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # Generate cache key
            if self.key_func:
                key = self.key_func(*args, **kwargs)
            else:
                # Default key generation
                key_data = f"{func.__name__}:{args}:{sorted(kwargs.items())}"
                key = hashlib.md5(key_data.encode()).hexdigest()

            # Try to get from cache
            cache_manager = get_cache_manager()
            cached_result = cache_manager.get(key, self.backend)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(key, result, self.ttl, self.backend)
            logger.debug(f"Cached result for {func.__name__}")
            return result

        return wrapper


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None

def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager

def set_cache_manager(manager: CacheManager) -> None:
    """Set the global cache manager instance."""
    global _cache_manager
    _cache_manager = manager

# Convenience functions
def cache_get(key: str, backend: Optional[str] = None) -> Optional[Any]:
    """Get value from cache."""
    return get_cache_manager().get(key, backend)

def cache_set(key: str, value: Any, ttl: Optional[int] = None, backend: Optional[str] = None) -> None:
    """Set value in cache."""
    get_cache_manager().set(key, value, ttl, backend)

def cache_delete(key: str, backend: Optional[str] = None) -> bool:
    """Delete from cache."""
    return get_cache_manager().delete(key, backend)

def cache_clear(backend: Optional[str] = None) -> None:
    """Clear cache."""
    get_cache_manager().clear(backend)

def cache_has_key(key: str, backend: Optional[str] = None) -> bool:
    """Check if key exists in cache."""
    return get_cache_manager().has_key(key, backend)

# LLM response caching
def cache_llm_response(provider: str, model: str, prompt: str, response: str, ttl: int = 3600) -> None:
    """Cache LLM response."""
    key = f"llm:{provider}:{model}:{hashlib.md5(prompt.encode()).hexdigest()}"
    cache_set(key, response, ttl)

def get_cached_llm_response(provider: str, model: str, prompt: str) -> Optional[str]:
    """Get cached LLM response."""
    key = f"llm:{provider}:{model}:{hashlib.md5(prompt.encode()).hexdigest()}"
    return cache_get(key)

# Tool result caching
def cache_tool_result(tool_name: str, params: Dict[str, Any], result: Any, ttl: int = 1800) -> None:
    """Cache tool execution result."""
    key = f"tool:{tool_name}:{hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()}"
    cache_set(key, result, ttl)

def get_cached_tool_result(tool_name: str, params: Dict[str, Any]) -> Optional[Any]:
    """Get cached tool result."""
    key = f"tool:{tool_name}:{hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()}"
    return cache_get(key)