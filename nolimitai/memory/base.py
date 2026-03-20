"""Base contract for memory backends.

This interface is backend-agnostic and can be implemented by in-memory cache,
Redis, or other key-value stores.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseMemory(ABC):
    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Store a value by key, optionally with an expiration time."""

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for key or default when key does not exist."""

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete key and return True if it existed."""

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Return True if key exists."""

    @abstractmethod
    def clear(self, namespace: Optional[str] = None) -> None:
        """Clear all keys or only keys in a namespace when provided."""