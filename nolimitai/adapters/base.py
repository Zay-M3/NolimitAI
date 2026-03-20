from abc import ABC, abstractmethod
from typing import AsyncIterator, Dict, List, Optional

class BaseAdapter(ABC):

    @abstractmethod
    async def chat(
        self,
        model: str,
        messages: List[Dict],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
    ) -> AsyncIterator[str]:
        """Streaming response for real-time UI."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns the name of the provider (e.g., 'groq')."""
        pass