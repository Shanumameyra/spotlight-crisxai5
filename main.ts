// Spotlight @crisxai5 entry for make.fun (Node 22, standard library only).
// It copies POST.json from the repository root to /output/POST.json, where the
// gate reads it. That is all the program has to do. The entry is the post
// itself: the agent made the spotlight card in-session, the card is posted
// natively on X from a public account with the text the rules ask for,
// POST.json names the post, and the house reads the post's counts from X.
// Nothing this program writes about the post is scored.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const SRC = join(BOT_DIR, 'POST.json');
const DEST = join(OUTPUT_DIR, 'POST.json');

// The repository is mounted read-only in the grader: never write to BOT_DIR.
// Only OUTPUT_DIR is written, and only after it exists. Every filesystem
// failure is caught (OSError) and reported with exit code 1.
try {
  mkdirSync(OUTPUT_DIR, { recursive: true });
} catch (err) {
  console.error(`Output directory could not be created at ${OUTPUT_DIR}: ${(err as Error).message}`);
  process.exit(1);
}

try {
  copyFileSync(SRC, DEST);
} catch (err) {
  console.error(`POST.json could not be copied from ${SRC}: ${(err as Error).message}`);
  process.exit(1);
}

// Deterministic byte check: the copied file must match the source exactly.
try {
  const srcBytes = readFileSync(SRC);
  const destBytes = readFileSync(DEST);
  if (!srcBytes.equals(destBytes)) {
    console.error('POST.json copy differs from the source; refusing to report success.');
    process.exit(1);
  }
} catch (err) {
  console.error(`POST.json could not be verified after copying: ${(err as Error).message}`);
  process.exit(1);
}
