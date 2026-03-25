import { Config, ConfigParams } from './config/config';
import { Router } from './core/router';

export class NolimitAI {
  /**
   * NolimitAI provides an interface to interact with multiple AI services through a unified API.
   * It uses a Router to manage request routing with a round-robin strategy.
   */
  
  private config: Config | null = null;
  private router: Router | null = null;

  constructor() {}

  /**
   * Set the configuration for NolimitAI.
   * This allows updating the configuration after initialization.
   */
  public setConfig(params: ConfigParams): void {
    const config = Config.setConfig(params);
    this.config = config;
    this.router = new Router(config);
  }

  /**
   * Returns the provider used in the latest successful response.
   */
  public getLastUsedService(): string | null {
    if (!this.router) {
      return null;
    }
    return this.router.getLastUsedService();
  }

  /**
   * Returns providers attempted in the latest chat cycle.
   */
  public getLastRouteTrace(): string[] {
    if (!this.router) {
      return [];
    }
    return this.router.getLastRouteTrace();
  }

  /**
   * Returns the next provider that would be selected.
   */
  public getNextService(): string | null {
    if (!this.router) {
      return null;
    }
    return this.router.getNextService();
  }

  /**
   * Routes the request to the appropriate AI service and yields the response in chunks.
   */
  public async *chat(
    prompt: string,
    model?: string,
    context?: any,
    sessionId: string = 'default',
    userId?: string
  ): AsyncIterable<string> {
    if (!this.router) {
      throw new Error('NolimitIA is not configured. Please call setConfig() before using chat().');
    }

    const stream = this.router.route(prompt, model, context, sessionId, userId);
    
    for await (const chunk of stream) {
      yield chunk;
    }
  }
}

export { Config };
export type { ConfigParams };
