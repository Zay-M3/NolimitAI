## NolimitAI

Goal: Developet a library in Python how a inteligent router for multiple providers of LLMs, it for evit the rate limit using a Round robin patron, unifyin a same format with streaming and keep the context of the conversation through of a multi-level momori (Cache, Redis and RAG)

first schema of folder architure
```bash
nolimit_ai/                   
├── __init__.py               
│
├── core/                     
│   ├── __init__.py
│   ├── router.py             # Orchestrates logic: receives prompts, requests turns, and calls the adapter
│   └── round_robin.py        # Pure rotation algorithm logic
│
├── adapters/                 # API connection implementations
│   ├── __init__.py
│   ├── base.py               # Abstract base class defining mandatory methods (e.g., `stream_chat`)
│   ├── groq_adapter.py       
│   └── openrouter_adapter.py 
│
├── memory/                 
│   ├── __init__.py
│   ├── base.py               
│   ├── cache.py              
│   └── redis.py              
│
└── config/                   
    ├── __init__.py
    └── settings.py           # Loads environment variables and API keys into the application
```

This proyect have a momory used in three caps, first using cache storate in Python, two using a connection to redis for cache of conext and three, using RAG strategy with vectorial database 


