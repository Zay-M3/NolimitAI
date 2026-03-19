## NolimitAI

Objetivo: Desarrollar una librería en Python que funcione como un enrutador inteligente para múltiples proveedores de LLMs, para evitar límites de tasa usando un patrón Round Robin, unificar un mismo formato con streaming y mantener el contexto de la conversación mediante una memoria multinivel (Cache, Redis y RAG).

Primer esquema de arquitectura de carpetas
```bash
nolimit_ai/
├── __init__.py
│
├── core/
│   ├── __init__.py
│   ├── router.py             # Orquesta la lógica: recibe prompts, solicita turnos y llama al adapter
│   └── round_robin.py        # Lógica pura del algoritmo de rotación
│
├── adapters/                 # Implementaciones de conexión a APIs
│   ├── __init__.py
│   ├── base.py               # Clase base abstracta que define métodos obligatorios (p. ej., `stream_chat`)
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
	└── settings.py           # Carga variables de entorno y claves API dentro de la aplicación
```

Este proyecto tiene una memoria usada en tres capas: primero usando almacenamiento en caché en Python, segundo usando una conexión a Redis para caché de contexto y tercero usando una estrategia RAG con base de datos vectorial.