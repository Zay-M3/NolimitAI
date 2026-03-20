## NolimitAI

NolimitAI es una librería Python que enruta solicitudes de chat entre múltiples proveedores LLM con round robin, hace streaming en tiempo real con iteradores asíncronos y conserva el contexto por sesión con cache en memoria.

Este documento describe lo que existe y funciona actualmente en el repositorio.

[Documentacion en ingles](./README.md)

Arquitectura actual
-------------------

```bash
NoLimitAI/
├── test.py                        # Script end-to-end interactivo (uso manual, no pytest)
├── nolimitai/
│   ├── api.py                     # Envoltura API con Router configurado
│   ├── nolimitai.py               # Clase principal NolimitAI con set_config() + chat() streaming
│   ├── adapters/
│   │   ├── base.py                # Contrato BaseAdapter (chat asíncrono en streaming)
│   │   ├── grop_adapter.py        # Adapter streaming de Groq
│   │   ├── openrouter_adapter.py  # Adapter streaming de OpenRouter
│   │   ├── adapters.py            # Mapa ADAPTERS_FACTORIES: servicio -> constructor
│   │   └── __init__.py
│   ├── config/
│   │   ├── config.py              # Dataclass de configuración (keys + parámetros)
│   │   └── __init__.py
│   ├── core/
│   │   ├── round_robin.py         # Implementación de rotación de servicios
│   │   ├── router.py              # Enrutamiento streaming + fallback + contexto de sesión
│   │   ├── errors.py              # Utilidades agnósticas para clasificar errores HTTP
│   │   └── __init__.py
│   └── memory/
│       ├── base.py                # Contrato de backend de memoria
│       ├── cache.py               # Backend cache en proceso con TTL
│       └── __init__.py
└── README_SPANIHS.md
```

Flujo de streaming (async for + yield)
--------------------------------------
1. El usuario consume `async for token in nlai.chat(...)`.
2. `NolimitAI.chat()` en `nolimitai/nolimitai.py` delega en `Router.route()`.
3. `Router.route()` elige proveedor con `RoundRobin.next()`.
4. Router crea el adapter con `ADAPTERS_FACTORIES`.
5. El adapter `chat()` entrega chunks/tokens en streaming.
6. Router re-emite cada chunk con `yield chunk`.
7. Router acumula la respuesta completa y la guarda en cache para mantener contexto.

Funcionamiento del router (actual)
----------------------------------
- Guarda mensajes por sesión con llaves:
    - `session:{session_id}:messages`
    - `user:{user_id}:session:{session_id}:messages`
- Agrega el prompt del usuario una sola vez antes de los intentos.
- Reintenta hasta `len(services)` proveedores.
- Política de fallback:
    - Si error es reintentable (`429`, `503`) o auth/permisos (`401`, `403`), rota al siguiente proveedor.
    - Si no es reintentable, relanza la excepción.
- Cuando hay éxito, agrega la respuesta del asistente al historial en cache.

Round robin
-----------
- Implementado en `nolimitai/core/round_robin.py`.
- Rota servicios en orden determinístico.
- Métodos disponibles: `next()`, `peek()`, `add()`, `remove()`, `reset()`, `snapshot()`.

Manejo de errores
-----------------
- Implementado en `nolimitai/core/errors.py`.
- Funciones:
    - `extract_status_code(exc)`
    - `is_retryable(exc)`
    - `is_auth_error(exc)`
- Soporta múltiples formas de excepción de SDKs (`status_code`, `code`, `response.status_code`).

Módulo memory 
----------------------------------
- Backend activo: cache en proceso (`nolimitai/memory/cache.py`).
- Usa diccionarios a nivel de módulo para compartir estado dentro del mismo proceso Python.
- Soporta TTL, `exists`, `delete`, `clear` y namespace.
- Soporte con Redis (Proximamente)

Adapters y clase base
---------------------
- `BaseAdapter` (`nolimitai/adapters/base.py`) define un contrato único de streaming:
    - `async def chat(...) -> AsyncIterator[str]`
- Adapters disponibles ahora:
    - `GropAdapter` (Groq)
    - `OpenRouterAdapter` (OpenRouter con cliente OpenAI y base_url de OpenRouter)
- `nolimitai/adapters/adapters.py` centraliza la creación de adapters con factories.

Configuración
-------------
- `Config` guarda:
    - vault de API keys (`_vault`)
    - parámetros globales de generación (`temperature`, `max_tokens`, `top_p`)
- `Config.set_config(...)` filtra keys para conservar solo servicios soportados.

Sobre test.py
-------------
- Se implementaran para probar una version para producción.

Uso rápido
----------
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

        async for token in app.chat(prompt="Hola", model="openai/gpt-oss-120b"):
                print(token, end="", flush=True)
        print()

asyncio.run(main())
```

Notas actuales
--------------
- El streaming en tiempo real está implementado de punta a punta con async iterators.
- El contexto por sesión está respaldado hoy por cache en memoria de proceso.
- Redis y RAG no están implementados todavía en este código actual.

