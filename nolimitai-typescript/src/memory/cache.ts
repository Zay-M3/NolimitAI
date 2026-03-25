import { BaseMemory } from "./base";

// Global storage to mimic Python's module-level dictionaries
const SESSION_CACHE = new Map<string, any>();
const SESSION_EXPIRES_AT = new Map<string, number>();

export class CacheMemory extends BaseMemory {
  private namespace: string;
  private sessionId: string;

  constructor(sessionId: string = "default", namespace: string = "default") {
    super();
    this.sessionId = sessionId;
    this.namespace = namespace;
  }

  private _fullKey(key: string, namespace?: string): string {
    const ns = namespace === undefined ? this.namespace : namespace;
    return `${ns}:${key}`;
  }

  private _isExpired(fullKey: string): boolean {
    const expiresAt = SESSION_EXPIRES_AT.get(fullKey);
    if (expiresAt === undefined) {
      return false;
    }
    return Date.now() / 1000 >= expiresAt;
  }

  private _purgeIfExpired(fullKey: string): void {
    if (this._isExpired(fullKey)) {
      SESSION_CACHE.delete(fullKey);
      SESSION_EXPIRES_AT.delete(fullKey);
    }
  }

  set(key: string, value: any, ttlSeconds?: number): void {
    const fullKey = this._fullKey(key);
    SESSION_CACHE.set(fullKey, value);

    if (ttlSeconds === undefined || ttlSeconds === null) {
      SESSION_EXPIRES_AT.delete(fullKey);
    } else {
      SESSION_EXPIRES_AT.set(fullKey, Date.now() / 1000 + Math.max(0, ttlSeconds));
    }
  }

  get(key: string, defaultValue: any = null): any {
    const fullKey = this._fullKey(key);
    this._purgeIfExpired(fullKey);
    if (!SESSION_CACHE.has(fullKey)) {
        return defaultValue;
    }
    return SESSION_CACHE.get(fullKey);
  }

  delete(key: string): boolean {
    const fullKey = this._fullKey(key);
    this._purgeIfExpired(fullKey);

    const existed = SESSION_CACHE.has(fullKey);
    SESSION_CACHE.delete(fullKey);
    SESSION_EXPIRES_AT.delete(fullKey);
    return existed;
  }

  exists(key: string): boolean {
    const fullKey = this._fullKey(key);
    this._purgeIfExpired(fullKey);
    return SESSION_CACHE.has(fullKey);
  }

  clear(namespace?: string): void {
    if (namespace === undefined) {
      SESSION_CACHE.clear();
      SESSION_EXPIRES_AT.clear();
      return;
    }

    const prefix = `${namespace}:`;
    const keysToRemove: string[] = [];
    for (const key of SESSION_CACHE.keys()) {
      if (key.startsWith(prefix)) {
        keysToRemove.push(key);
      }
    }

    for (const key of keysToRemove) {
      SESSION_CACHE.delete(key);
      SESSION_EXPIRES_AT.delete(key);
    }
  }
}
