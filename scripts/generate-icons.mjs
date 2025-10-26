// Generate favicon.ico and PNG icons from public/favicon.svg
// Requires: sharp, to-ico
import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
import toIco from 'to-ico';

const root = path.resolve(process.cwd());
const publicDir = path.join(root, 'public');
const srcSvg = path.join(publicDir, 'favicon.svg');

async function ensurePublicDir() {
  await fs.mkdir(publicDir, { recursive: true });
}

async function generatePng(size, outName) {
  const svg = await fs.readFile(srcSvg);
  const outPath = path.join(publicDir, outName);
  await sharp(svg).resize(size, size, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } }).png({ compressionLevel: 9 }).toFile(outPath);
  return outPath;
}

async function generateFaviconIco() {
  const svg = await fs.readFile(srcSvg);
  const sizes = [16, 32, 48];
  const pngBuffers = await Promise.all(
    sizes.map(async (s) => await sharp(svg).resize(s, s, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 0 } }).png().toBuffer())
  );
  const ico = await toIco(pngBuffers);
  const outPath = path.join(publicDir, 'favicon.ico');
  await fs.writeFile(outPath, ico);
}

async function generateOgImage() {
  // Create a simple 1200x630 image with a dark gradient-like background and centered icon
  const width = 1200, height = 630;
  const bg = {
    create: {
      width,
      height,
      channels: 4,
      background: { r: 20, g: 60, b: 140, alpha: 1 }
    }
  };
  const bgImg = sharp(bg).png();

  const svg = await fs.readFile(srcSvg);
  const iconPng = await sharp(svg).resize(256, 256).png().toBuffer();

  const composed = await bgImg
    .composite([
      { input: iconPng, left: Math.round(width / 2 - 128), top: Math.round(height / 2 - 128) }
    ])
    .png()
    .toBuffer();

  const outPath = path.join(publicDir, 'og-image.png');
  await fs.writeFile(outPath, composed);
}

async function main() {
  await ensurePublicDir();
  const pngMap = [
    [16, 'favicon-16x16.png'],
    [32, 'favicon-32x32.png'],
    [48, 'favicon-48x48.png'],
    [64, 'favicon-64x64.png'],
    [180, 'apple-touch-icon.png'],
    [192, 'android-chrome-192x192.png'],
    [512, 'android-chrome-512x512.png']
  ];

  for (const [size, name] of pngMap) {
    await generatePng(size, name);
  }

  await generateFaviconIco();
  await generateOgImage();
  console.log('Icons generated into public/.');
}

main().catch((err) => { console.error(err); process.exit(1); });
