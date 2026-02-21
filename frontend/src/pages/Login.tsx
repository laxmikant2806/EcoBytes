import { useState } from "react";
import { login, register } from "../services/auth";

type Mode = "login" | "register";

export default function Login() {

  const [mode, setMode]         = useState<Mode>("login");
  const [name, setName]         = useState("");
  const [email, setEmail]       = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Client-side validation
    if (mode === "register" && !name.trim()) {
      setError("Please enter your full name.");
      return;
    }
    if (mode === "register" && password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setLoading(true);
    try {
      if (mode === "register") {
        await register({ name: name.trim(), email, password });
        // Hard navigate so useAuthProfile re-initializes with the new token.
        // React Router navigate() keeps the hook mounted with stale null user state.
        window.location.href = "/onboarding";
      } else {
        await login({ email, password });
        // Hard navigate so useAuthProfile re-reads the token from localStorage.
        window.location.href = "/";
      }
    } catch (err: unknown) {
      setLoading(false);
      const message = err instanceof Error ? err.message : "Something went wrong. Please try again.";
      // Make common backend messages friendlier
      if (message.includes("already exists")) {
        setError("An account with this email already exists. Try signing in instead.");
      } else if (message.includes("Invalid email or password")) {
        setError("Incorrect email or password. Please try again.");
      } else {
        setError(message);
      }
    }
  };

  const switchMode = (next: Mode) => {
    setMode(next);
    setError(null);
    setName("");
    setPassword("");
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-terra-50 px-4">
      <div className="w-full max-w-sm rounded-2xl bg-white p-8 shadow-lg">

        {/* Brand */}
        <div className="mb-6 flex flex-col items-center gap-2">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-terra-500 shadow-md">
            <span className="text-3xl font-bold text-white">T</span>
          </div>
          <h1 className="text-2xl font-bold text-terra-900">TerraScore</h1>
          <p className="text-center text-sm text-gray-500">
            Track and reward your environmental impact.
          </p>
        </div>

        {/* Mode tabs */}
        <div className="mb-6 flex rounded-xl bg-gray-100 p-1">
          <button
            type="button"
            onClick={() => switchMode("login")}
            className={`flex-1 rounded-lg py-2 text-sm font-semibold transition ${
              mode === "login"
                ? "bg-white text-terra-700 shadow"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            Sign In
          </button>
          <button
            type="button"
            onClick={() => switchMode("register")}
            className={`flex-1 rounded-lg py-2 text-sm font-semibold transition ${
              mode === "register"
                ? "bg-white text-terra-700 shadow"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            Create Account
          </button>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">

          {/* Name — register only */}
          {mode === "register" && (
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">
                Full Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Priya Sharma"
                required
                autoComplete="name"
                className="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-terra-400"
              />
            </div>
          )}

          {/* Email */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
              autoComplete="email"
              className="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-terra-400"
            />
          </div>

          {/* Password */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={mode === "register" ? "Min. 8 characters" : "Your password"}
              required
              autoComplete={mode === "register" ? "new-password" : "current-password"}
              className="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-terra-400"
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-terra-500 py-3 font-semibold text-white transition hover:bg-terra-600 active:scale-95 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? (
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" />
            ) : null}
            {loading
              ? mode === "register" ? "Creating account…" : "Signing in…"
              : mode === "register" ? "Create Account" : "Sign In"
            }
          </button>
        </form>

        <p className="mt-6 text-center text-xs text-gray-400">
          By continuing you agree to our Terms of Service and Privacy Policy.
        </p>
      </div>
    </div>
  );
}
