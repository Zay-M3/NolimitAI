# NolimitAI TypeScript

<p align="center">
  <img src="../assets/nolimitai_logo.png" alt="NolimitAI Logo" width="600"/>
</p>

This is a complete TypeScript port of the `nolimitai` Python package.

Check the full documentation [Documentation](https://github.com/Zay-M3/NolimitAI/blob/main/README.md)

## Installation

```bash
npm install nolimitai-typescript
# or
bun add nolimitai-typescript
```

## Configuration

This package uses `openai` and `groq-sdk` libraries.
The configuration is handled via the `Config` class, which accepts an object with API keys.

## Usage

```typescript
import { NolimitAI } from 'nolimitai-typescript';

const ai = new NolimitAI();

ai.setConfig({
  keys: {
    groq: process.env.GROQ_API_KEY,
    gemini_ai: process.env.GEMINI_API_KEY,
    // ... other providers
  },
  temperature: 0.7,
});

const stream = ai.chat("Tell me a joke");

for await (const chunk of stream) {
  process.stdout.write(chunk);
}
```

## License

Apache-2.0

## Running Tests

To verify the implementation with a mock adapter:

```bash
bun run test
# or
npx tsx test.ts
```

## Type Checking

```bash
bun run check
# or
npx tsc --noEmit
```

## Architecture

- `src/core/`: Core logic (Router, RoundRobin, Errors).
- `src/adapters/`: Provider implementations (Gemini, Groq, Mistral, OpenRouter, Together).
- `src/config/`: Configuration management.
- `src/memory/`: Memory/Cache implementations.
- `src/utils/`: Utilities (async-openai factory).
