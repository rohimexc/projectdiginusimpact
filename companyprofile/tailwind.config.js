/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#4F46E5",
        primaryDark: "#4338CA",
        secondary: "#EEF2FF",
        cream: "#F8FAFC",
        dark: "#0F172A",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
}