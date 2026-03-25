export interface ConfigParams {
  temperature?: number;
  maxTokens?: number;
  topP?: number;
  keys?: Record<string, string>;
}

export class Config {
  public readonly temperature?: number;
  public readonly maxTokens?: number;
  public readonly topP?: number;

  private static readonly SUPPORTED_SERVICES = [
    'groq', 'openrouter', 'together_ai', 'gemini_ai', 'mistral_ai'
  ];

  private readonly _vault: Record<string, string>;

  private constructor(params: ConfigParams) {
    this.temperature = params.temperature;
    this.maxTokens = params.maxTokens;
    this.topP = params.topP;
    this._vault = params.keys || {};
  }

  public static setConfig(params: ConfigParams): Config {
    const keys = params.keys || {};
    const validKeys: Record<string, string> = {};

    for (const [service, key] of Object.entries(keys)) {
      if (Config.SUPPORTED_SERVICES.includes(service)) {
        validKeys[service] = key;
      }
    }

    return new Config({
      ...params,
      keys: validKeys
    });
  }

  public getAvailableServices(): string[] {
    return Object.keys(this._vault);
  }

  public getKey(service: string): string {
    if (!this._vault[service]) {
      throw new Error(`Service '${service}' is not configured.`);
    }
    return this._vault[service];
  }
}
