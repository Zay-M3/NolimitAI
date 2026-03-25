/**
 * Round Robin selection utilities.
 */
export class RoundRobin<T> {
  private _items: T[] = [];
  private _index: number = 0;

  constructor(items: T[] = []) {
    this._items = [...items];
  }

  public get length(): number {
    return this._items.length;
  }

  public get isEmpty(): boolean {
    return this._items.length === 0;
  }

  public next(): T {
    if (this.isEmpty) {
      throw new Error("RoundRobin has no items.");
    }

    const item = this._items[this._index];
    this._index = (this._index + 1) % this._items.length;
    return item;
  }

  public peek(): T {
    if (this.isEmpty) {
      throw new Error("RoundRobin has no items.");
    }
    return this._items[this._index];
  }

  public add(item: T): void {
    this._items.push(item);
  }

  public remove(item: T): void {
    if (this.isEmpty) {
      throw new Error("RoundRobin has no items.");
    }

    const removedIndex = this._items.indexOf(item);
    if (removedIndex === -1) {
      throw new Error(`Item '${item}' not found in RoundRobin.`);
    }

    this._items.splice(removedIndex, 1);

    if (this.isEmpty) {
      this._index = 0;
      return;
    }

    if (removedIndex < this._index) {
      this._index--;
    }

    this._index %= this._items.length;
  }

  public reset(): void {
    this._index = 0;
  }

  public snapshot(): T[] {
    return [...this._items];
  }

  public [Symbol.iterator](): Iterator<T> {
    return this._items[Symbol.iterator]();
  }
}
