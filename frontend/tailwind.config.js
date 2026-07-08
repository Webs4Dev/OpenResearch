/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        surface: {
          0: "#FFFFFF",
          1: "#F7F7F5",
          2: "#F0EFEC",
        },
        border: {
          DEFAULT: "#E5E3DE",
          strong: "#D4D1C9",
          accent: "#3B7A64",
        },
        text: {
          primary: "#1F1E1C",
          secondary: "#6B6862",
          muted: "#9C988F",
          accent: "#3B7A64",
          success: "#0F7A5C",
          warning: "#9A6A1E",
        },
        chip: {
          amber: "#FAEEDA",
          "amber-text": "#9A6A1E",
          teal: "#E1F5EE",
          "teal-text": "#085041",
          success: "#E3F3EA",
        },
      },
      borderRadius: {
        DEFAULT: "8px",
      },
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "sans-serif",
        ],
      },
    },
  },
  plugins: [],
};
