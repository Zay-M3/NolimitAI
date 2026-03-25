import Groq from 'groq-sdk';
import { BaseAdapter, AdapterOptions } from './base';

export class GroqAdapter extends BaseAdapter {
  private client: Groq;

  constructor(apiKey: string, defaultOptions: AdapterOptions) {
    super(apiKey, defaultOptions);
    this.client = new Groq({
      apiKey: apiKey,
    });
  }

  async *chat(
    model: string,
    messages: Array<{ role: string; content: string }> = [],
    temperature: number,
    maxTokens: number,
    topP: number
  ): AsyncIterable<string> {
    const effectiveModel = model ?? this.defaultOptions.model; 
    const effectiveTemperature = temperature ?? this.defaultOptions.temperature;
    const effectiveMaxTokens = maxTokens ?? this.defaultOptions.maxTokens;
    const effectiveTopP = topP ?? this.defaultOptions.topP;

    const groqMessages = messages.map(m => ({
      role: m.role as 'user' | 'assistant' | 'system',
      content: m.content
    }));

    const stream = await this.client.chat.completions.create({
      model: effectiveModel,
      messages: groqMessages,
      temperature: effectiveTemperature,
      max_tokens: effectiveMaxTokens,
      top_p: effectiveTopP,
      stream: true,
    });

    for await (const chunk of stream) {
      const content = chunk.choices[0]?.delta?.content || '';
      if (content) {
        yield content;
      }
    }
    
  }

  get providerName(): string {
    return 'groq';
  }
}
