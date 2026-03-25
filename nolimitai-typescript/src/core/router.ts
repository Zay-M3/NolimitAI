import { Config } from '../config/config';
import { RoundRobin } from './round-robin';
import { isRetryable, isAuthError } from './errors';
import { CacheMemory } from '../memory/cache';
import { ADAPTERS_FACTORIES, AdapterOptions } from '../adapters/index';

export class Router {
  private config: Config;
  private cache: CacheMemory;
  private sessionTtlSeconds: number;
  private services: string[];
  private roundRobin: RoundRobin<string>;
  private _lastUsedService: string | null = null;
  private _lastRouteTrace: string[] = [];

  constructor(config: Config) {
    this.config = config;
    this.cache = new CacheMemory();
    this.sessionTtlSeconds = 3600;
    this.services = this.config.getAvailableServices();
    this.roundRobin = new RoundRobin(this.services);
  }

  public getLastUsedService(): string | null {
    return this._lastUsedService;
  }

  public getLastRouteTrace(): string[] {
    return [...this._lastRouteTrace];
  }

  public getNextService(): string | null {
    if (this.roundRobin.isEmpty) {
      return null;
    }
    return this.roundRobin.peek();
  }

  private _messagesCacheKey(sessionId: string, userId?: string): string {
    if (userId) {
      return `user:${userId}:session:${sessionId}:messages`;
    }
    return `session:${sessionId}:messages`;
  }

  public getSessionMessages(sessionId: string, userId?: string): Array<any> {
    const cacheKey = this._messagesCacheKey(sessionId, userId);
    const messages = this.cache.get(cacheKey, []);
    if (!Array.isArray(messages)) {
      return [];
    }
    return messages;
  }

  public async *route(
    prompt: string,
    model?: string,
    context?: any,
    sessionId: string = 'default',
    userId?: string
  ): AsyncIterable<string> {
    if (this.roundRobin.isEmpty) {
      throw new Error('No services available to route the task.');
    }

    let attempts = 0;
    const maxAttempts = this.services.length;
    this._lastRouteTrace = [];

    const cacheKey = this._messagesCacheKey(sessionId, userId);
    const messages = [...this.getSessionMessages(sessionId, userId)];

    let contentText = prompt || '';
    if (context) {
      contentText = `Context: ${JSON.stringify(context)}\n\nUser Question: ${prompt}`;
    }

    const message: any = { role: 'user', content: contentText };
    if (context) {
      message.context = context;
    }
    messages.push(message);

    while (attempts < maxAttempts) {
      const service = this.roundRobin.next();
      this._lastRouteTrace.push(service);

      // In case service list changed dynamically (not fully supported here but matching logic)
      if (!this.services.includes(service)) {
        attempts++;
        continue;
      }

      const factory = ADAPTERS_FACTORIES[service];
      if (!factory) {
        throw new Error(`No adapter found for service '${service}'.`);
      }

      const targetModel = model;

      const options: AdapterOptions = {
        model: targetModel,
        temperature: this.config.temperature,
        maxTokens: this.config.maxTokens,
        topP: this.config.topP,
      };

      const apiKey = this.config.getKey(service);
      const adapter = factory(apiKey, options);

      let fullResponse = '';
      let startedStreaming = false;

      try {
        const stream = adapter.chat(targetModel, messages, options.temperature, options.maxTokens, options.topP);

        for await (const chunk of stream) {
          startedStreaming = true;
          this._lastUsedService = service;
          fullResponse += chunk;
          yield chunk;
        }

        messages.push({ role: 'assistant', content: fullResponse });
        this.cache.set(cacheKey, messages, this.sessionTtlSeconds);
        return;

      } catch (e: any) {
        if (startedStreaming) {
          throw e;
        }

        if (isRetryable(e) || isAuthError(e)) {  
          attempts++;
          continue;
        }
        throw e;
      }
    }

    throw new Error('All services failed to process the request after multiple attempts.');
  }
}
