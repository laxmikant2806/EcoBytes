/// <reference types="vite/client" />

/**
 * Single source of truth for all environment-variable-backed config.
 * All VITE_* vars are replaced at build time by Vite — they are safe to bundle.
 *
 * Throws a clear error at startup if any required variable is missing,
 * rather than failing silently later with a cryptic Firebase error.
 */

function requireEnv(key: string): string {
  const value = import.meta.env[key] as string | undefined;
  if (!value) {
    throw new Error(
      `Missing required environment variable: ${key}\n` +
        `Copy frontend/.env.example to frontend/.env and fill in all values.`
    );
  }
  return value;
}

export const config = {
  firebase: {
    apiKey:            requireEnv("VITE_FIREBASE_API_KEY"),
    authDomain:        requireEnv("VITE_FIREBASE_AUTH_DOMAIN"),
    projectId:         requireEnv("VITE_FIREBASE_PROJECT_ID"),
    storageBucket:     requireEnv("VITE_FIREBASE_STORAGE_BUCKET"),
    messagingSenderId: requireEnv("VITE_FIREBASE_MESSAGING_SENDER_ID"),
    appId:             requireEnv("VITE_FIREBASE_APP_ID"),
    measurementId:     import.meta.env["VITE_FIREBASE_MEASUREMENT_ID"] as string | undefined,
  },
  api: {
    baseUrl: (import.meta.env["VITE_API_BASE_URL"] as string) ?? "http://localhost:8000/api/v1",
  },
} as const;
