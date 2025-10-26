import fs from 'node:fs/promises';
import path from 'node:path';

const root = path.resolve(process.cwd());
const srcDir = path.join(root, 'public');
const destDir = path.join(root, 'Version-1', 'public');

const files = [
  'favicon.ico',
  'favicon.svg',
  'favicon-16x16.png',
  'favicon-32x32.png',
  'favicon-48x48.png',
  'favicon-64x64.png',
  'apple-touch-icon.png',
  'android-chrome-192x192.png',
  'android-chrome-512x512.png',
  'og-image.png',
  'site.webmanifest'
];

async function main() {
  await fs.mkdir(destDir, { recursive: true });
  for (const f of files) {
    try {
      const src = path.join(srcDir, f);
      const dest = path.join(destDir, f);
      const data = await fs.readFile(src);
      await fs.writeFile(dest, data);
      console.log('Synced', f);
    } catch (e) {
      console.warn('Skip (not found):', f);
    }
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
