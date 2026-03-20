"""Simple in-memory cache backend.

Data is stored in module-level dictionaries so it is shared across instances
within the same Python process session.
"""

from time import time
from typing import Any, Dict, Optional

from nolimitai.memory.base import BaseMemory


_SESSION_CACHE: Dict[str, Any] = {}
_SESSION_EXPIRES_AT: Dict[str, float] = {}


class CacheMemory(BaseMemory):
	def __init__(self, session_id: str = "default", namespace: str = "default") -> None:
		self.namespace = namespace
		self.session_id = session_id

	def _full_key(self, key: str, namespace: Optional[str] = None) -> str:
		ns = self.namespace if namespace is None else namespace
		return f"{ns}:{key}"

	def _is_expired(self, full_key: str) -> bool:
		expires_at = _SESSION_EXPIRES_AT.get(full_key)
		if expires_at is None:
			return False
		return time() >= expires_at

	def _purge_if_expired(self, full_key: str) -> None:
		if self._is_expired(full_key):
			_SESSION_CACHE.pop(full_key, None)
			_SESSION_EXPIRES_AT.pop(full_key, None)

	def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
		full_key = self._full_key(key)
		_SESSION_CACHE[full_key] = value

		if ttl_seconds is None:
			_SESSION_EXPIRES_AT.pop(full_key, None)
		else:
			_SESSION_EXPIRES_AT[full_key] = time() + max(0, ttl_seconds)

	def get(self, key: str, default: Any = None) -> Any:
		full_key = self._full_key(key)
		self._purge_if_expired(full_key)
		return _SESSION_CACHE.get(full_key, default)

	def delete(self, key: str) -> bool:
		full_key = self._full_key(key)
		self._purge_if_expired(full_key)

		existed = full_key in _SESSION_CACHE
		_SESSION_CACHE.pop(full_key, None)
		_SESSION_EXPIRES_AT.pop(full_key, None)
		return existed

	def exists(self, key: str) -> bool:
		full_key = self._full_key(key)
		self._purge_if_expired(full_key)
		return full_key in _SESSION_CACHE

	def clear(self, namespace: Optional[str] = None) -> None:
		if namespace is None:
			_SESSION_CACHE.clear()
			_SESSION_EXPIRES_AT.clear()
			return

		prefix = f"{namespace}:"
		keys_to_remove = [k for k in _SESSION_CACHE if k.startswith(prefix)]
		for key in keys_to_remove:
			_SESSION_CACHE.pop(key, None)
			_SESSION_EXPIRES_AT.pop(key, None)
