/**
 * useAuthProfile
 *
 * Reads the JWT from localStorage, decodes the user, then fetches the
 * backend profile (/users/me). Drives routing in App.tsx:
 *   no token / expired token  → /login
 *   valid token, no profile   → /onboarding
 *   valid token + profile     → /dashboard (or requested route)
 *
 * No Firebase auth state subscription needed — JWT is synchronously
 * available in localStorage on first render, so there is no async
 * "waiting for auth to initialize" delay.
 *
 * Double-fetch guard: isFetchingRef prevents concurrent calls to
 * fetchProfile (React StrictMode double-invokes effects in dev).
 */

import { useEffect, useRef, useState } from "react";
import api from "../services/api";
import { getCurrentUser, logout } from "../services/auth";
import type { AuthUser, UserProfile } from "../types";

export interface AuthProfileState {
  user: AuthUser | null;
  profile: UserProfile | null;
  loading: boolean;
  error: string | null;
  refreshProfile: () => Promise<void>;
}

export function useAuthProfile(): AuthProfileState {
  // Decode user synchronously from JWT on first render — no async wait.
  const [user, setUser] = useState<AuthUser | null>(() => getCurrentUser());
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [profileError, setProfileError] = useState<string | null>(null);

  // Guard: prevent concurrent /users/me calls (React StrictMode double-invoke).
  const isFetchingRef = useRef(false);
  const mountedRef = useRef(true);

  useEffect(() => {
    mountedRef.current = true;
    return () => { mountedRef.current = false; };
  }, []);

  /**
   * Fetch the backend profile for the signed-in user.
   * The JWT is attached automatically by the Axios interceptor in api.ts.
   */
  const fetchProfile = async () => {
    if (isFetchingRef.current || !mountedRef.current) return;
    isFetchingRef.current = true;

    try {
      const res = await api.get<UserProfile>("/users/me");
      if (mountedRef.current) {
        setProfile(res.data);
        setProfileError(null);
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);

      // 401 or 403 → token is invalid/expired or unauthorized → force logout so user goes to /login.
      const shouldLogout =
        message.includes("401") ||
        message.includes("403") ||
        message.toLowerCase().includes("unauthorized") ||
        message.toLowerCase().includes("not authenticated");

      if (shouldLogout) {
        console.warn("[useAuthProfile] Auth error detected, logging out:", message);
        logout(); // clears token + hard redirects to /login
        return;
      }

      // 404 → no profile yet → route to /onboarding (expected path for new users).
      const isNotFound =
        message.includes("404") || message.toLowerCase().includes("not found");

      if (mountedRef.current) {
        setProfile(null);
        if (!isNotFound) {
          console.error("[useAuthProfile] fetchProfile error:", message);
          setProfileError(message);
        }
      }
    } finally {
      isFetchingRef.current = false;
      if (mountedRef.current) setLoading(false);
    }
  };

  useEffect(() => {
    const currentUser = getCurrentUser();
    if (!mountedRef.current) return;

    if (!currentUser) {
      // No token or token expired — not authenticated.
      setUser(null);
      setLoading(false);
      return;
    }

    // Token is valid — set user and fetch profile.
    setUser(currentUser);
    fetchProfile();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const refreshProfile = async () => {
    isFetchingRef.current = false; // allow a forced refresh
    setLoading(true);
    await fetchProfile();
  };

  return {
    user,
    profile,
    loading,
    error: profileError,
    refreshProfile,
  };
}
