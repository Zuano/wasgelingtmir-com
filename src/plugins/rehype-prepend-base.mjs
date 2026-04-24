// Rehype-Plugin: Hängt den Base-Path vor alle absoluten internen Links.
// Rehype plugin: prepends base path to absolute internal links.
import { visit } from "unist-util-visit";

const ATTRS_PER_TAG = {
  a: "href",
  img: "src",
  source: "src",
  video: "src",
  audio: "src",
  link: "href",
  script: "src",
};

/**
 * Factory für das rehype-Plugin.
 * @param {{ base?: string }} [options]
 */
export default function rehypePrependBase(options = {}) {
  const base = (options.base ?? "").replace(/\/+$/, "");

  // Das eigentliche Transformer-Callback – muss den tree in-place modifizieren
  // und NICHTS zurückgeben (oder den tree selbst).
  return (tree) => {
    if (!base) return;
    visit(tree, "element", (node) => {
      if (!node.properties) return;
      const attr = ATTRS_PER_TAG[node.tagName];
      if (attr) {
        const value = node.properties[attr];
        if (
          typeof value === "string" &&
          value.startsWith("/") &&
          !value.startsWith("//") &&
          !value.startsWith(`${base}/`) &&
          value !== base
        ) {
          node.properties[attr] = `${base}${value}`;
        }
      }
      if (typeof node.properties.srcset === "string") {
        node.properties.srcset = node.properties.srcset
          .split(",")
          .map((part) => {
            const trimmed = part.trim();
            if (
              !trimmed.startsWith("/") ||
              trimmed.startsWith("//") ||
              trimmed.startsWith(`${base}/`)
            ) {
              return trimmed;
            }
            const spaceIdx = trimmed.indexOf(" ");
            const url = spaceIdx === -1 ? trimmed : trimmed.slice(0, spaceIdx);
            const rest = spaceIdx === -1 ? "" : trimmed.slice(spaceIdx);
            return `${base}${url}${rest}`;
          })
          .join(", ");
      }
    });
  };
}
