// Usage / Aufruf: node scripts/make-og-image.mjs public/og-default.png
// Generates public/og-default.png (1200x630) / Erzeugt das Standard-Vorschaubild
import sharp from "sharp";
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f18f44"/><stop offset="100%" stop-color="#de5815"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="#fef7ee"/>
  <rect x="0" y="0" width="1200" height="14" fill="url(#g)"/>
  <rect x="96" y="150" width="150" height="150" rx="33" fill="url(#g)"/>
  <text x="171" y="252" font-family="Georgia, serif" font-weight="700" font-size="84" fill="#fff" text-anchor="middle">w</text>
  <text x="96" y="410" font-family="Georgia, serif" font-weight="700" font-size="84" fill="#1c1917">wasgelingtmir.com</text>
  <text x="96" y="480" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" font-size="36" fill="#57534e">Tipps zu Apple, Gesundheit, Ernährung und Leben</text>
  <text x="96" y="545" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" font-size="28" fill="#b84214">Persönliche Antworten von Zuano aus Österreich</text>
</svg>`;
await sharp(Buffer.from(svg)).png({ compressionLevel: 9 }).toFile(process.argv[2]);
