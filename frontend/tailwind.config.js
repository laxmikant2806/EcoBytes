/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        terra: {
          50:  "#f0fdf4",
          100: "#dcfce7",
          200: "#bbf7d0",
          300: "#86efac",
          400: "#4ade80",
          500: "#22c55e",  // primary action green
          600: "#16a34a",
          700: "#15803d",
          800: "#166534",
          900: "#14532d",  // deep forest
          950: "#052e16",
        },
        earth: {
          100: "#fef9c3",
          500: "#ca8a04",  // warm amber for points/rewards
          900: "#713f12",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
