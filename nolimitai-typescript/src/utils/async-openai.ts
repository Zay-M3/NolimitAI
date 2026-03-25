import OpenAI from 'openai';

/**
 * Factory to create an OpenAI client instance with specific configuration.
 * useful for providers compatible with OpenAI API (OpenRouter, Together, Mistral, Gemini via OpenAI adapter).
 */
export const createOpenAIClient = (apiKey: string, baseURL?: string): OpenAI => {
  return new OpenAI({
    apiKey: apiKey,
    baseURL: baseURL,
  });
};
