// Hilfsfunktion zum Erzeugen interner URLs, die korrekt mit dem Base-Path arbeiten.
// Helper for creating internal URLs that respect Astro's configured base path.
// Bei DNS-Umstellung auf wasgelingtmir.com wird der Base-Path leer,
// und `link("/blog")` liefert einfach "/blog" – kein Code-Diff nötig.
const RAW_BASE = import.meta.env.BASE_URL ?? "/";

function normalizeBase(base: string): string {
  // "/wasgelingtmir-com/" → "/wasgelingtmir-com"
  // "/" → "" (damit link("/blog") auch "/blog" ergibt, nicht "//blog")
  if (base === "/" || base === "") return "";
  return base.endsWith("/") ? base.slice(0, -1) : base;
}

const BASE = normalizeBase(RAW_BASE);

/**
 * Erzeugt einen absoluten Pfad (relativ zum Host) mit korrektem Base-Prefix.
 * Builds an absolute (host-relative) URL prefixed with the site base path.
 *
 * @example
 *   link("/blog") // "/wasgelingtmir-com/blog" oder "/blog" je nach Config
 *   link("blog") // "/wasgelingtmir-com/blog" oder "/blog"
 */
export function link(path: string): string {
  if (!path) return BASE || "/";
  // Externe URLs oder Anker unverändert zurückgeben
  if (/^(?:[a-z]+:)?\/\//i.test(path) || path.startsWith("#") || path.startsWith("mailto:")) {
    return path;
  }
  const clean = path.startsWith("/") ? path : `/${path}`;
  return `${BASE}${clean}` || "/";
}

/**
 * Prüft, ob ein Pfad mit einem bestimmten internen Route-Segment beginnt.
 * Berücksichtigt den Base-Path.
 */
export function isActive(currentPath: string, targetPath: string): boolean {
  const fullTarget = link(targetPath);
  if (fullTarget === link("/")) {
    return currentPath === fullTarget || currentPath === `${fullTarget}/`;
  }
  return currentPath.startsWith(fullTarget);
}
