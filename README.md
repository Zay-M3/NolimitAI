# NoLimitAI

<p align="center">
  <img src="assets/nolimitai_logo.png" alt="NolimitAI Logo" width="600"/>
</p>

<p align="center">
  <a href="https://pypi.org/project/nolimitai/"><img src="https://img.shields.io/pypi/v/nolimitai?color=blue" alt="PyPI version"></a>
  <a href="https://pypi.org/project/nolimitai/"><img src="https://img.shields.io/pypi/pyversions/nolimitai" alt="Python versions"></a>
  <a href="https://pypi.org/project/nolimitai/"><img src="https://img.shields.io/pypi/dm/nolimitai" alt="Downloads"></a>
  <a href="https://github.com/Zay-M3/nolimitai/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/nolimitai" alt="License"></a>
</p>


NoLimitAI is a Python library designated to route LLM requests across multiple providers (Groq, OpenRouter, Together AI, Gemini, Mistral) with built-in round-robin load balancing and automatic failover. It simplifies managing multiple AI services through a single, unified asynchronous API.

## Features

- **Multi-Provider Support**: Seamlessly switch between Groq, OpenRouter, Together AI, Google Gemini, and Mistral AI.
- **Round-Robin & Fallback**: Automatically rotates through configured providers to distribute load and handles failures by retrying with the next available service.
- **Async Streaming**: Native `async`/`await` support with streaming responses.
- **Unified Interface**: Use one standard API for all providers.

## Installation

Install the package from PyPI:

```bash
pip install nolimitai
```

You can view the project on PyPI here: [https://pypi.org/project/nolimitai/](https://pypi.org/project/nolimitai/)

## Usage

Here is a complete example of how to configure and use NoLimitAI.

### 1. Basic Setup

You need to provide API keys for the services you want to use. The library does not automatically load environment variables; you must pass them explicitly.

```python
import asyncio
import os
from nolimitai import NolimitAI

# Optional: Load environment variables from a .env file
# from dotenv import load_dotenv
# load_dotenv()

async def main():
    # Initialize the client
    nlai = NolimitAI()

    # Configure the client with your API keys and optional parameters
    # You only need to provide keys for the services you intend to use.
    nlai.set_config(
        temperature=0.7,
        max_tokens=1024,
        top_p=0.9,
        keys={
            "groq": os.getenv("GROQ_API_KEY"),
            "openrouter": os.getenv("OPENROUTER_API_KEY"),
            "gemini_ai": os.getenv("GEMINI_API_KEY"),
            "mistral_ai": os.getenv("MISTRAL_API_KEY"),
            "together_ai": os.getenv("TOGETHER_API_KEY"),
        }
    )

    prompt = "Explain the concept of round-robin scheduling in one sentence."

    print(f"--- Asking: {prompt} ---\n")

    # Check which service is next in line (optional)
    next_service = nlai.get_next_service()
    print(f"[Next Service]: {next_service}")

    try:
        # Stream the response
        print("[Response]: ", end="", flush=True)
        async for token in nlai.chat(prompt=prompt):
            print(token, end="", flush=True)
        print("\n")
        
        # Check which service actually handled the request
        used_service = nlai.get_last_used_service()
        print(f"[Used Service]: {used_service}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Configuration Options

The `set_config` method accepts the following parameters:

- `temperature` (float): Sampling temperature (0.0 to 1.0).
- `max_tokens` (int): Maximum number of tokens to generate.
- `top_p` (float): Nucleus sampling parameter.
- `keys` (dict): A dictionary mapping provider names to API keys.

**Supported Keys:**
- `"groq"`
- `"openrouter"`
- `"together_ai"`
- `"gemini_ai"`
- `"mistral_ai"`

## Important Notes

- **Failover**: If a service fails to connect or authorize, the router will automatically try the next configured service in the list.

## Troubleshooting

- **`RuntimeError: NoLimitIA no ha sido configurado`**: This error occurs if you try to call `chat()` before calling `set_config()`. Ensure you configure the instance with at least one valid API key.
- **Authentication Errors**: Ensure your API keys are correct. If a key is invalid, the router will treat it as a failure and attempt to switch to another provider if available.

## License

This project is licensed under the Apache-2.0 License.

[Documentación en español](./README_SPANIHS.md)
