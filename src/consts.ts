// Zentrale Konstanten für die ganze Website
// Central site constants

export const SITE = {
  title: "wasgelingtmir.com",
  tagline: "Antworten finden – Tipps zu Apple, Gesundheit, Ernährung und Leben",
  description:
    "Persönliche Antworten, Tipps und Erkenntnisse rund um Apple-Geräte, Gesundheit, Ernährung und Alltag. Gesammelt von Zuano aus Österreich.",
  author: "Zuano",
  url: "https://wasgelingtmir.com",
  email: "04kleeblatt-ansporn@icloud.com",
  locale: "de-AT",
  language: "de",
} as const;

export type CategorySlug =
  | "apple-mac"
  | "web-dienste"
  | "gesundheit"
  | "ernaehrung"
  | "leben-gedanken";

export interface CategoryInfo {
  slug: CategorySlug;
  name: string;
  shortName: string;
  description: string;
  color: string;
  icon: string;
}

export const CATEGORIES: Record<CategorySlug, CategoryInfo> = {
  "apple-mac": {
    slug: "apple-mac",
    name: "Apple & Mac",
    shortName: "Apple",
    description:
      "Tipps und Tricks rund um iPhone, iPad, Mac und Apple-Dienste – aus dem Alltag eines engagierten Apple-Nutzers.",
    color: "slate",
    icon: "M17.05 20.28c-.98.95-2.05.88-3.08.4-1.09-.5-2.08-.48-3.24 0-1.44.62-2.2.44-3.06-.4C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09M12 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25",
  },
  "web-dienste": {
    slug: "web-dienste",
    name: "Web & Dienste",
    shortName: "Web",
    description:
      "Alles rund um Online-Dienste, Shopping, Kommunikation und Web-Tools – was im digitalen Alltag wirklich hilft.",
    color: "blue",
    icon: "M12 2a10 10 0 100 20 10 10 0 000-20zm0 2c1.58 0 3.05.38 4.34 1.03l-1.71 1.71A7 7 0 0012 4zm-2 7h4v2h-4v-2zm-4-3h12v2H6V8z",
  },
  gesundheit: {
    slug: "gesundheit",
    name: "Gesundheit",
    shortName: "Gesundheit",
    description:
      "Beiträge zu Schlaf, Fitness, Körper und Wohlbefinden – aus eigener Erfahrung und echten Veränderungen.",
    color: "emerald",
    icon: "M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z",
  },
  ernaehrung: {
    slug: "ernaehrung",
    name: "Ernährung",
    shortName: "Ernährung",
    description:
      "Gedanken und Erkenntnisse rund um bewusste Ernährung, regionale Produkte und gesunde Entscheidungen.",
    color: "amber",
    icon: "M12 2a5 5 0 015 5c0 1.47-.63 2.79-1.64 3.72C17.11 11.7 18 13.74 18 16a6 6 0 11-12 0c0-2.26.89-4.3 2.64-5.28A5 5 0 0112 2z",
  },
  "leben-gedanken": {
    slug: "leben-gedanken",
    name: "Leben & Gedanken",
    shortName: "Leben",
    description:
      "Persönliche Reflexionen, Bücher und inspirierende Geschichten – für den Kopf und fürs Herz.",
    color: "rose",
    icon: "M21 5h-2V3H5v2H3v14h2v2h14v-2h2V5zm-2 12H5V7h14v10z",
  },
};

export const NAVIGATION = [
  { label: "Start", href: "/" },
  { label: "Alle Artikel", href: "/blog" },
  ...Object.values(CATEGORIES).map((cat) => ({
    label: cat.shortName,
    href: `/kategorie/${cat.slug}`,
  })),
  { label: "Über", href: "/ueber-mich" },
] as const;

export const POSTS_PER_PAGE = 10;
