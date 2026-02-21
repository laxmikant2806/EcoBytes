/**
 * Custom JWT authentication helpers.
 * Firebase Auth has been removed. Authentication is now email + password
 * with JWTs issued by the FastAPI backend (/api/v1/auth/register and /login).
 *
 * Token storage: localStorage (key: "terrascore_token").
 * Token is a standard HS256 JWT — decoded client-side for the user payload
 * and expiry check (no sensitive data inside, signing is verified server-side).
 *
 * All components and hooks import from here — never call the API directly.
 */

import type { AuthUser } from "../types";
import api from "./api";

import { TOKEN_KEY } from "../constants";

// ── Token storage helpers ──────────────────────────────────────

export function saveToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

// ── JWT decode (client-side, no signature verification) ────────

interface JwtPayload {
  sub: string;
  email: string;
  name: string;
  exp: number;
  iat: number;
}

/**
 * Decode the JWT payload without verifying the signature.
 * Signature verification happens on the backend on every protected request.
 * Returns null if the token is missing, malformed, or expired.
 */
export function decodeToken(token: string): JwtPayload | null {
  try {
    const parts = token.split(".");
    if (parts.length !== 3) return null;
    // JWT parts are base64url encoded — replace URL-safe chars and pad
    const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const padded = base64.padEnd(base64.length + (4 - (base64.length % 4)) % 4, "=");
    const payload: JwtPayload = JSON.parse(atob(padded));
    // Check expiry
    if (payload.exp && Date.now() / 1000 > payload.exp) return null;
    return payload;
  } catch {
    return null;
  }
}

// ── Read current user from stored token ────────────────────────

/**
 * Return the currently authenticated user decoded from the stored JWT.
 * Returns null if no token or token is expired.
 */
export function getCurrentUser(): AuthUser | null {
  const token = getToken();
  if (!token) return null;
  const payload = decodeToken(token);
  if (!payload) return null;
  return { uid: payload.sub, email: payload.email, name: payload.name };
}

// ── API calls ──────────────────────────────────────────────────

interface LoginPayload {
  email: string;
  password: string;
}

interface RegisterPayload {
  email: string;
  password: string;
  name: string;
}

interface TokenResponse {
  access_token: string;
  token_type: string;
  uid: string;
  email: string;
  name: string;
}

/**
 * Register a new account.
 * Stores the returned JWT and returns the AuthUser.
 */
export async function register(payload: RegisterPayload): Promise<AuthUser> {
  const { data } = await api.post<TokenResponse>("/auth/register", payload);
  saveToken(data.access_token);
  return { uid: data.uid, email: data.email, name: data.name };
}

/**
 * Log in with email + password.
 * Stores the returned JWT and returns the AuthUser.
 */
export async function login(payload: LoginPayload): Promise<AuthUser> {
  const { data } = await api.post<TokenResponse>("/auth/login", payload);
  saveToken(data.access_token);
  return { uid: data.uid, email: data.email, name: data.name };
}

/**
 * Log out: clear token and hard-navigate to /login.
 * Hard navigation (not React Router) ensures all React state is wiped.
 */
export function logout(): void {
  clearToken();
  window.location.href = "/login";
}
