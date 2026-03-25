import { BaseAdapter, AdapterOptions } from './base';
import { createOpenAIClient } from '../utils/async-openai';
import OpenAI from 'openai';

export class MistralAdapter extends BaseAdapter {
  private client: OpenAI;
  private readonly baseUrl = 'https://api.mistral.ai/v1';

  constructor(apiKey: string, defaultOptions: AdapterOptions) {
    super(apiKey, defaultOptions);
    this.client = createOpenAIClient(apiKey, this.baseUrl);
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

    const openaiMessages = messages.map(m => ({
      role: m.role as 'user' | 'assistant' | 'system',
      content: m.content
    }));

    const stream = await this.client.chat.completions.create({
      model: effectiveModel,
      messages: openaiMessages,
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
    return 'mistral_ai';
  }
}
