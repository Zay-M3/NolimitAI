from nolimitai.adapters.base import BaseAdapter
from openai import AsyncOpenAI as OpenAI
from typing import AsyncIterator, Optional


class MistralAIAdapter(BaseAdapter):
    
    def __init__(
        self,
        api_key: str,
        default_model: str,
        default_temperature: float = 0.7,
        default_max_tokens: int = 2048,
        default_top_p: float = 0.8,
    ):
        self.api_key = api_key
        self.default_model = default_model
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        self.default_top_p = default_top_p
        self.client = OpenAI(
            base_url="https://api.mistral.ai/v1",
            api_key=self.api_key)
        
    async def chat(
        self,
        model: str,
        messages: list,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
    ) -> AsyncIterator[str]:
        """Streams the response from the Mistral AI API."""
        effective_model = self.default_model if model is None else model
        effective_temperature = self.default_temperature if temperature is None else temperature
        effective_max_tokens = self.default_max_tokens if max_tokens is None else max_tokens
        effective_top_p = self.default_top_p if top_p is None else top_p

        response = await self.client.chat.completions.create(
            model=effective_model,
            messages=messages,
            temperature=effective_temperature,
            max_tokens=effective_max_tokens,
            top_p=effective_top_p,
            reasoning_effort="medium",
            stream=True,
            stop=None,
        )
        
        async for chunk in response:
            yield (chunk.choices[0].delta.content or "")

    @property
    def provider_name(self) -> str:
        return "mistral_ai"