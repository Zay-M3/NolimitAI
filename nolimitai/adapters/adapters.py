from typing import Callable, Dict, Any

from .gemini_ai_adapter import GeminiAIAdapter
from .mistral_ai_adapter import MistralAIAdapter
from .together_ia_adapter import TogetherAIAdapter
from .grop_adapter import GropAdapter
from .openrouter_adapter import OpenRouterAdapter

AdapterFactory = Callable[..., Any]

ADAPTERS_FACTORIES: Dict[str, AdapterFactory] = {
    "groq": lambda api_key, **opts: GropAdapter(
        api_key=api_key,
        default_model=opts.get("model", "llama-3.3-70b-versatile"),
        default_temperature=opts.get("temperature", 0.7),
        default_max_tokens=opts.get("max_tokens", 2048),
        default_top_p=opts.get("top_p", 0.8),
    ),
    "openrouter": lambda api_key, **opts: OpenRouterAdapter(
        api_key=api_key,
        default_model=opts.get("model", "google/gemini-flash-1.5-exp"),
        default_temperature=opts.get("temperature", 0.7),
        default_max_tokens=opts.get("max_tokens", 2048),
        default_top_p=opts.get("top_p", 0.8),
    ),
    "together_ai": lambda api_key, **opts: TogetherAIAdapter(
        api_key=api_key,
        default_model=opts.get("model", "meta-llama/Llama-3.3-70B-Instruct-Turbo"),
        default_temperature=opts.get("temperature", 0.7),
        default_max_tokens=opts.get("max_tokens", 2048),
        default_top_p=opts.get("top_p", 0.8),
    ),
    "gemini_ai": lambda api_key, **opts: GeminiAIAdapter(
        api_key=api_key,
        default_model=opts.get("model", "gemini-1.5-flash"),
        default_temperature=opts.get("temperature", 0.7),
        default_max_tokens=opts.get("max_tokens", 2048),
        default_top_p=opts.get("top_p", 0.8),
    ),
    "mistral_ai": lambda api_key, **opts: MistralAIAdapter(
        api_key=api_key,
        default_model=opts.get("model", "mistral-small-latest"),
        default_temperature=opts.get("temperature", 0.7),
        default_max_tokens=opts.get("max_tokens", 2048),
        default_top_p=opts.get("top_p", 0.8),
    ),
}