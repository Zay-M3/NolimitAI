from typing import Callable, Dict, Any
from .grop_adapter import GropAdapter
from .openrouter_adapter import OpenRouterAdapter

AdapterFactory = Callable[..., Any]

ADAPTERS_FACTORIES: Dict[str, AdapterFactory] = {
    "groq": lambda api_key, **opts: GropAdapter(
        api_key=api_key,
        default_temperature=opts.get("temperature", 0.7),
        default_max_tokens=opts.get("max_tokens", 2048),
        default_top_p=opts.get("top_p", 0.8),
    ),
    "openrouter": lambda api_key, **opts: OpenRouterAdapter(
        api_key=api_key,
        default_temperature=opts.get("temperature", 0.7),
        default_max_tokens=opts.get("max_tokens", 2048),
        default_top_p=opts.get("top_p", 0.8),
    ),
}