// Astro Content Collections – Schema für Artikel und Seiten
// Astro content collections – schemas for blog posts and pages
import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string().default(""),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    category: z.string(),
    categorySlug: z.enum([
      "apple-mac",
      "web-dienste",
      "gesundheit",
      "ernaehrung",
      "leben-gedanken",
    ]),
    tags: z.array(z.string()).default([]),
    slug: z.string().optional(),
    heroImage: z.string().optional(),
    heroImageAlt: z.string().optional(),
    draft: z.boolean().default(false),
    originalUrl: z.string().url().optional(),
    wordpressId: z.string().optional(),
    outdated: z.boolean().default(false),
    outdatedNote: z.string().optional(),
  }),
});

const pages = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/pages" }),
  schema: z.object({
    title: z.string(),
    description: z.string().default(""),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    slug: z.string().optional(),
    type: z.literal("page").default("page"),
    originalUrl: z.string().url().optional(),
  }),
});

export const collections = { blog, pages };
