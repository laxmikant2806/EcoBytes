import { useState } from "react";
import type { AuthUser } from "../types";
import api from "../services/api";

const INTEREST_OPTIONS = [
  { value: "tree_planting", label: "🌳 Tree Planting" },
  { value: "waste_cleanup", label: "🗑️ Waste Cleanup" },
  { value: "recycling", label: "♻️ Recycling" },
  { value: "composting", label: "🌿 Composting" },
  { value: "water_conservation", label: "💧 Water Conservation" },
  { value: "energy_saving", label: "⚡ Energy Saving" },
  { value: "cycling", label: "🚴 Cycling" },
  { value: "public_transport", label: "🚌 Public Transport" },
  { value: "sustainable_purchase", label: "🛍️ Sustainable Shopping" },
  { value: "carpooling", label: "🚗 Carpooling" },
];

interface OnboardingProps {
  user: AuthUser;
  /** Called by App.tsx after profile creation so it re-fetches and routes to / */
  onComplete: () => Promise<void>;
}

export default function Onboarding({ user, onComplete }: OnboardingProps) {
  const [name, setName] = useState(user.name ?? "");
  const [area, setArea] = useState("");
  const [contact, setContact] = useState(user.email ?? "");
  const [bio, setBio] = useState("");
  const [interests, setInterests] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const toggleInterest = (value: string) => {
    setInterests((prev) =>
      prev.includes(value) ? prev.filter((i) => i !== value) : [...prev, value]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!name.trim()) { setError("Name is required."); return; }
    if (!area.trim()) { setError("City / area is required."); return; }
    if (!contact.trim()) { setError("Contact (email or phone) is required."); return; }

    setSubmitting(true);
    try {
      await api.post("/users/", {
        uid: user.uid,
        name: name.trim(),
        area: area.trim(),
        contact: contact.trim(),
        bio: bio.trim(),
        interests,
      });
      // Re-fetch profile in App.tsx — this will switch the route to /
      await onComplete();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-terra-50 px-4 py-10">
      <div className="w-full max-w-lg rounded-2xl bg-white p-8 shadow-lg">

        {/* Header */}
        <div className="mb-6 text-center">
          <div className="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-terra-500">
            <span className="text-2xl font-bold text-white">T</span>
          </div>
          <h1 className="text-2xl font-bold text-terra-900">Welcome to TerraScore!</h1>
          <p className="mt-1 text-sm text-gray-500">
            Set up your profile to start tracking your eco impact.
          </p>
        </div>

        {error && (
          <div className="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">

          {/* Name */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Full Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Priya Sharma"
              required
              className="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-terra-400"
            />
          </div>

          {/* City / Area */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              City / Area <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={area}
              onChange={(e) => setArea(e.target.value)}
              placeholder="e.g. Mumbai, Pune, Bengaluru…"
              required
              className="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-terra-400"
            />
          </div>

          {/* Contact */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Contact (email or phone) <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={contact}
              onChange={(e) => setContact(e.target.value)}
              placeholder="your@email.com or +91 98765 43210"
              required
              className="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-terra-400"
            />
          </div>

          {/* Bio */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Bio <span className="text-gray-400 font-normal">(optional)</span>
            </label>
            <textarea
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              placeholder="Tell the community a bit about your eco journey…"
              rows={3}
              className="w-full rounded-xl border border-gray-200 bg-gray-50 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-terra-400 resize-none"
            />
          </div>

          {/* Interests */}
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700">
              Eco Interests <span className="text-gray-400 font-normal">(pick any)</span>
            </label>
            <div className="flex flex-wrap gap-2">
              {INTEREST_OPTIONS.map((opt) => {
                const selected = interests.includes(opt.value);
                return (
                  <button
                    key={opt.value}
                    type="button"
                    onClick={() => toggleInterest(opt.value)}
                    className={`rounded-full px-3 py-1.5 text-sm font-medium transition ${selected
                        ? "bg-terra-500 text-white shadow"
                        : "bg-gray-100 text-gray-600 hover:bg-terra-100"
                      }`}
                  >
                    {opt.label}
                  </button>
                );
              })}
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full rounded-xl bg-terra-500 py-3 font-semibold text-white transition hover:bg-terra-600 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {submitting ? "Creating your profile…" : "Complete Setup →"}
          </button>
        </form>
      </div>
    </div>
  );
}
