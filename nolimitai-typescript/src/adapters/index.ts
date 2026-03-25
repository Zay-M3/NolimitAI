import { BaseAdapter, AdapterOptions } from './base';
import { GeminiAIAdapter } from './gemini-adapter';
import { GroqAdapter } from './groq-adapter';
import { MistralAdapter } from './mistral-adapter';
import { OpenRouterAdapter } from './openrouter-adapter';
import { TogetherAdapter } from './together-adapter';

export type AdapterFactory = (apiKey: string, options: AdapterOptions) => BaseAdapter;

export const ADAPTERS_FACTORIES: Record<string, AdapterFactory> = {
  groq: (apiKey, { 
    model = "openai/gpt-oss-120b", 
    temperature = 0.5, 
    maxTokens = 1024, 
    topP = 1 
  } = {}) => new GroqAdapter(apiKey, { model, temperature, maxTokens, topP }),
  openrouter: (apiKey, { 
    model = "openrouter/free", 
    temperature = 0.7, 
    maxTokens = 2048, 
    topP = 0.8 
  } = {}) => new OpenRouterAdapter(apiKey, { model, temperature, maxTokens, topP }),
  together_ai: (apiKey, { 
    model = "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", 
    temperature = 0.7, 
    maxTokens = 2048, 
    topP = 0.8 
  } = {}) => new TogetherAdapter(apiKey, { model, temperature, maxTokens, topP }),
  gemini_ai: (apiKey, { 
    model = "gemini-3-flash-preview", 
    temperature = 0.7, 
    maxTokens = 2048, 
    topP = 0.8 
  } = {}) => new GeminiAIAdapter(apiKey, { model, temperature, maxTokens, topP }),
  mistral_ai: (apiKey, { 
    model = "mistral-medium-latest", 
    temperature = 0.7, 
    maxTokens = 2048, 
    topP = 0.8 
  } = {}) => new MistralAdapter(apiKey, { model, temperature, maxTokens, topP }),
};

export { BaseAdapter, GeminiAIAdapter, GroqAdapter, MistralAdapter, OpenRouterAdapter, TogetherAdapter };
export type { AdapterOptions };
