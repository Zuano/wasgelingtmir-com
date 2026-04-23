// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";

// Finale Website-URL (wichtig für RSS + Sitemap)
// Final site URL (used by RSS and sitemap)
const SITE_URL = "https://wasgelingtmir.com";

export default defineConfig({
  site: SITE_URL,

  // Qualitativ hochwertige Bildoptimierung / high-quality image optimization
  image: {
    // sharp wird automatisch verwendet / sharp is used automatically
  },

  // Tailwind v4 via Vite Plugin
  vite: {
    plugins: [tailwindcss()],
  },

  integrations: [
    // Sitemap.xml für Suchmaschinen / XML sitemap for search engines
    sitemap({
      i18n: undefined,
      changefreq: "monthly",
      priority: 0.7,
    }),
  ],

  // Saubere, sprechende URLs / clean, speaking URLs
  trailingSlash: "ignore",
  build: {
    format: "directory",
  },

  // Prefetch von verlinkten Seiten beim Hovern / prefetch on hover
  prefetch: {
    defaultStrategy: "hover",
  },
});
