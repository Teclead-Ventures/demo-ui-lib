// Usage: npx tsx scripts/firecrawl-page.ts <url> <output-path>
import Firecrawl from '@mendable/firecrawl-js';
import { writeFileSync, mkdirSync, appendFileSync, readFileSync } from 'fs';
import { dirname } from 'path';
import { config } from 'dotenv';

config({ path: '.env.local' });

const apiKey = process.env.FIRECRAWL_API_KEY;
if (!apiKey) { console.error("Set FIRECRAWL_API_KEY in .env.local"); process.exit(1); }

const app = new Firecrawl({ apiKey });
const fc = app.v1; // v4 SDK uses .v1 sub-object for scrapeUrl
const url = process.argv[2];
const outputPath = process.argv[3];

if (!url || !outputPath) { console.error("Usage: npx tsx scripts/firecrawl-page.ts <url> <output-path>"); process.exit(1); }

async function main() {
  // Budget check: warn if >20 scrapes this month
  const usageLog = 'research/ergo-site/firecrawl-usage.log';
  try {
    const lines = readFileSync(usageLog, 'utf-8').split('\n').filter(Boolean);
    if (lines.length >= 20) {
      console.warn(`WARNING: ${lines.length} Firecrawl scrapes already logged. Free tier is ~500/month.`);
    }
  } catch {}

  const result = await fc.scrapeUrl(url, { formats: ['markdown', 'html'] });

  if (!result.success) {
    console.error(`Firecrawl error for ${url}:`, (result as any).error || 'unknown error');
    process.exit(1);
  }

  mkdirSync(dirname(outputPath), { recursive: true });
  writeFileSync(outputPath + '.md', result.markdown || '');
  writeFileSync(outputPath + '.html', result.html || '');
  writeFileSync(outputPath + '.json', JSON.stringify(result, null, 2));

  // Log usage
  mkdirSync('research/ergo-site', { recursive: true });
  appendFileSync(usageLog, `${new Date().toISOString()} ${url} SUCCESS\n`);

  console.log(`Saved: ${outputPath}.md, .html, .json (${result.markdown?.length || 0} chars)`);
}

main().catch(err => { console.error(err); process.exit(1); });
