// Standard AsyncIterable is global in TS with ES2018 lib.

export interface AdapterOptions {
  model?: string;
  temperature?: number;
  maxTokens?: number;
  topP?: number;
}

export abstract class BaseAdapter {
  protected apiKey: string;
  protected defaultOptions: AdapterOptions;

  constructor(apiKey: string, defaultOptions: AdapterOptions) {
    this.apiKey = apiKey;
    this.defaultOptions = defaultOptions;
  }

  /**
   * Streaming response for real-time UI.
   * Returns an AsyncIterator of strings.
   */
  abstract chat(
    model?: string,
    messages?: Array<{ role: string; content: string }>,
    temperature?: number,
    maxTokens?: number,
    topP?: number
  ): AsyncIterable<string>;

  /**
   * Returns the name of the provider (e.g., 'groq').
   */
  abstract get providerName(): string;
}
