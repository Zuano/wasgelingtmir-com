// @ts-check
import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";
import rehypePrependBase from "./src/plugins/rehype-prepend-base.mjs";

// Wenn CUSTOM_DOMAIN=true → wir deployen auf wasgelingtmir.com (Root-Domain)
// Andernfalls → GitHub-Pages-Unterordner zuano.github.io/wasgelingtmir-com
// Beim DNS-Umzug einfach CUSTOM_DOMAIN=true setzen (oder Default ändern).
//
// If CUSTOM_DOMAIN=true we deploy to wasgelingtmir.com (root), otherwise
// to the GitHub-Pages subfolder. At DNS switchover set CUSTOM_DOMAIN=true.
const USE_CUSTOM_DOMAIN = process.env.CUSTOM_DOMAIN === "true";

const SITE_URL = USE_CUSTOM_DOMAIN
  ? "https://wasgelingtmir.com"
  : "https://zuano.github.io";

const BASE_PATH = USE_CUSTOM_DOMAIN ? "/" : "/wasgelingtmir-com/";
// Ohne trailing slash für das Rehype-Plugin / stripped trailing slash for plugin
const BASE_WITHOUT_SLASH = BASE_PATH.replace(/\/+$/, "");

export default defineConfig({
  site: SITE_URL,
  base: BASE_PATH,
  trailingSlash: "ignore",

  // Markdown: alle absoluten internen Links (/images/..., /blog/... etc.)
  // bekommen automatisch den Base-Path vorangestellt.
  markdown: {
    rehypePlugins: BASE_WITHOUT_SLASH
      ? [[rehypePrependBase, { base: BASE_WITHOUT_SLASH }]]
      : [],
  },

  vite: {
    plugins: [tailwindcss()],
  },

  integrations: [
    sitemap({
      changefreq: "monthly",
      priority: 0.7,
    }),
  ],

  build: {
    format: "directory",
  },

  prefetch: {
    defaultStrategy: "hover",
  },
});
