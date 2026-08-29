/**
 * Central API client with automatic mock-data fallback.
 *
 * When VITE_API_BASE_URL is set and reachable, requests go to the Python
 * FastAPI backend. Otherwise, the mock services produce realistic sample
 * results so the frontend is fully demonstrable on its own.
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
const TIMEOUT_MS = 12000

export const isBackendConfigured = Boolean(BASE_URL)

async function apiRequest<T>(
  endpoint: string,
  body: unknown,
  mockFn: () => T,
): Promise<T> {
  // No backend configured — use mock data directly.
  if (!isBackendConfigured) {
    return simulateNetwork(mockFn)
  }

  try {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS)

    const res = await fetch(`${BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: controller.signal,
    })

    clearTimeout(timeout)

    if (!res.ok) {
      throw new Error(`Request failed: ${res.status}`)
    }
    return (await res.json()) as T
  } catch (err) {
    // Backend unreachable — gracefully fall back to mock data.
    console.warn(
      `[api] ${endpoint} failed, using mock data:`,
      err instanceof Error ? err.message : err,
    )
    return simulateNetwork(mockFn)
  }
}

function simulateNetwork<T>(fn: () => T): Promise<T> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(fn()), 700 + Math.random() * 500)
  })
}

export { apiRequest }
