## NolimitAI

NolimitAI is a Python library that routes chat requests across multiple LLM providers using round robin, streams tokens in real time with async iterators, and keeps conversation history in memory cache per session.

This document describes what is implemented and working in the repository right now.

[Spanish documentation](./README_SPANIHS.md)

Current architecture
--------------------

```bash
NoLimitAI/
├── test.py                        # Interactive end-to-end script (manual usage, not pytest)
├── nolimitai/
│   ├── api.py                     # API wrapper with configured Router instance
│   ├── nolimitai.py               # Main NolimitAI class with set_config() + chat() streaming
│   ├── adapters/
│   │   ├── base.py                # BaseAdapter contract (async streaming chat)
│   │   ├── grop_adapter.py        # Groq streaming adapter
│   │   ├── openrouter_adapter.py  # OpenRouter streaming adapter
│   │   ├── adapters.py            # ADAPTERS_FACTORIES map service -> adapter constructor
│   │   └── __init__.py
│   ├── config/
│   │   ├── config.py              # Config dataclass (keys + generation params)
│   │   └── __init__.py
│   ├── core/
│   │   ├── round_robin.py         # Service rotation implementation
│   │   ├── router.py              # Streaming routing + fallback + session context cache
│   │   ├── errors.py              # Provider-agnostic status/error classification
│   │   └── __init__.py
│   └── memory/
│       ├── base.py                # Memory backend contract
│       ├── cache.py               # In-process TTL cache backend
│       └── __init__.py
└── README.md
```

Streaming flow (async for + yield)
----------------------------------
1. User code iterates `async for token in nlai.chat(...)`.
2. `NolimitAI.chat()` in `nolimitai/nolimitai.py` forwards the request to `Router.route()`.
3. `Router.route()` selects a provider via `RoundRobin.next()`.
4. Router creates the adapter from `ADAPTERS_FACTORIES`.
5. Adapter `chat()` yields chunks/tokens as they arrive from provider streaming.
6. Router forwards each chunk with `yield chunk`.
7. Router also accumulates full assistant text and stores it in cache for session continuity.

Router behavior (current)
-------------------------
- Keeps session messages in cache with key pattern:
    - `session:{session_id}:messages`
    - `user:{user_id}:session:{session_id}:messages`
- Appends the user prompt once before provider attempts.
- Retries up to the number of configured services.
- Fallback policy:
    - On retryable errors (`429`, `503`) or auth/permission errors (`401`, `403`), rotates to next provider.
    - On non-retryable exceptions, raises immediately.
- On success, appends assistant response to cached conversation history.

Round robin behavior
--------------------
- Implemented in `nolimitai/core/round_robin.py`.
- Rotates over configured services in deterministic order.
- Supports `next()`, `peek()`, `add()`, `remove()`, `reset()`, and `snapshot()`.

Error handling module
---------------------
- Implemented in `nolimitai/core/errors.py`.
- Provides provider-agnostic helpers:
    - `extract_status_code(exc)`
    - `is_retryable(exc)`
    - `is_auth_error(exc)`
- Works with multiple SDK error shapes (`status_code`, `code`, `response.status_code`).

Memory module
--------------------------------
- Active backend: in-process cache (`nolimitai/memory/cache.py`).
- Shared module-level dictionaries make context persistent across instances in the same Python process.
- Supports TTL expiration, exists/delete/clear, and namespaced keys.
- Redis support (Coming soon)

Adapters and base contract
--------------------------
- `BaseAdapter` (`nolimitai/adapters/base.py`) defines a single streaming contract:
    - `async def chat(...) -> AsyncIterator[str]`
- Concrete adapters currently available:
    - `GropAdapter` (Groq)
    - `OpenRouterAdapter` (OpenRouter via OpenAI client with OpenRouter base URL)
- Factory registry in `nolimitai/adapters/adapters.py` builds adapters from service name + options.

Configuration module
--------------------
- `Config` dataclass stores:
    - API key vault (`_vault`)
    - generation defaults (`temperature`, `max_tokens`, `top_p`)
- `Config.set_config(...)` filters provided keys to supported services only.

test.py (important)
-------------------
- These will be implemented to test a production version.

Quick usage
-----------
```python
import asyncio
from nolimitai import NolimitAI

async def main():
        app = NolimitAI()
        app.set_config(
                temperature=0.8,
                max_tokens=1024,
                top_p=0.9,
                keys={
                        "groq": "YOUR_GROQ_KEY",
                        "openrouter": "YOUR_OPENROUTER_KEY",
                },
        )

        async for token in app.chat(prompt="Hello", model="openai/gpt-oss-120b"):
                print(token, end="", flush=True)
        print()

asyncio.run(main())
```

Current notes
-------------
- Real-time streaming is implemented end-to-end using async iterators.
- Session context is currently backed by in-process cache only.
- Redis and RAG are not implemented yet in this codebase.

