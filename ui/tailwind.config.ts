import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        "steel-azure": "#054a91",
        "steel-blue": "#3e7cb1",
        "alice-blue": "#dbe4ee",
        "harvest-orange": "#f17300",
        primary: "#054a91",
        secondary: "#3e7cb1",
        accent: "#f17300",
      },
    },
  },
  plugins: [],
};
export default config;
