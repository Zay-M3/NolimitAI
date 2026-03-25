/**
 * Base contract for memory backends.
 */
export abstract class BaseMemory {
  abstract set(key: string, value: any, ttlSeconds?: number): void;
  abstract get(key: string, defaultValue?: any): any;
  abstract delete(key: string): boolean;
  abstract exists(key: string): boolean;
  abstract clear(namespace?: string): void;
}
