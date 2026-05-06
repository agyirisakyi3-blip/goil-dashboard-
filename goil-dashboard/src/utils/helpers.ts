export function formatGhs(value: number): string {
  if (typeof value !== 'number' || isNaN(value)) return 'GHS 0';
  if (value >= 1e9) return `GHS ${(value / 1e9).toFixed(2)}B`;
  if (value >= 1e6) return `GHS ${(value / 1e6).toFixed(2)}M`;
  if (value >= 1e3) return `GHS ${(value / 1e3).toFixed(2)}K`;
  return `GHS ${value.toLocaleString()}`;
}

export async function loadJson<T>(filename: string, retries = 2): Promise<T> {
  for (let i = 0; i <= retries; i++) {
    try {
      const response = await fetch(`/data/${filename}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    } catch (err) {
      if (i === retries) throw new Error(`Failed to load ${filename}`);
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
  throw new Error(`Failed to load ${filename}`);
}
