from nolimitai.adapters.base import BaseAdapter
from groq import Groq
from typing import AsyncIterator, Optional


class GropAdapter(BaseAdapter):
    
    def __init__(
        self,
        api_key: str,
        default_temperature: float = 0.7,
        default_max_tokens: int = 2048,
        default_top_p: float = 0.8,
    ):
        self.api_key = api_key
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.default_top_p = default_top_p
        self.client = Groq(api_key=self.api_key)

    async def chat(
        self,
        messages: list,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        model: str = "groq/groq-2b",  
    ) -> AsyncIterator[str]:
        """Streams the response from the Groq API."""
        effective_temperature = self.default_temperature if temperature is None else temperature
        effective_max_tokens = self.default_max_tokens if max_tokens is None else max_tokens
        effective_top_p = self.default_top_p if top_p is None else top_p

        response = self.client.chat.completions.create(
            model=model, 
            messages=messages,
            temperature=effective_temperature,
            max_tokens=effective_max_tokens,
            top_p=effective_top_p,
            reasoning_effort="medium",
            stream=True,
            stop=None,
        )
        
        for chunk in response:
            yield (chunk.choices[0].delta.content or "")

    @property
    def provider_name(self) -> str:
        return "groq"