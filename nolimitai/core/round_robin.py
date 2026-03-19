"""Round Robin selection utilities.

This module contains a small, reusable round robin implementation that can be
used to rotate across providers, workers, or any list of items.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Iterable, Iterator, List, TypeVar


T = TypeVar("T")


@dataclass
class RoundRobin(Generic[T]):
	"""Simple round robin iterator over a mutable list of items.

	Example:
		rr = RoundRobin(["groq", "openrouter"])
		rr.next()  # "groq"
		rr.next()  # "openrouter"
		rr.next()  # "groq"
	"""

	items: Iterable[T] = field(default_factory=list)

	def __post_init__(self) -> None:
		self._items: List[T] = list(self.items)
		self._index: int = 0

	def __len__(self) -> int:
		return len(self._items)

	def __iter__(self) -> Iterator[T]:
		return iter(self._items)

	def __next__(self) -> T:
		if self.is_empty:
			raise StopIteration
		return self.next()

	@property
	def is_empty(self) -> bool:
		"""Return True when there are no items to rotate."""
		return len(self._items) == 0

	def next(self) -> T:
		"""Return the next item and advance the internal pointer."""
		if self.is_empty:
			raise ValueError("RoundRobin has no items.")

		item = self._items[self._index]
		self._index = (self._index + 1) % len(self._items)
		return item

	def peek(self) -> T:
		"""Return the next item without advancing the pointer."""
		if self.is_empty:
			raise ValueError("RoundRobin has no items.")
		return self._items[self._index]

	def add(self, item: T) -> None:
		"""Append a new item to the rotation."""
		self._items.append(item)

	def remove(self, item: T) -> None:
		"""Remove an item and keep pointer alignment stable."""
		if self.is_empty:
			raise ValueError("RoundRobin has no items.")

		removed_index = self._items.index(item)
		self._items.pop(removed_index)

		if self.is_empty:
			self._index = 0
			return

		if removed_index < self._index:
			self._index -= 1

		self._index %= len(self._items)

	def reset(self) -> None:
		"""Reset the pointer to the first item."""
		self._index = 0

	def snapshot(self) -> List[T]:
		"""Return a shallow copy of current items."""
		return list(self._items)
