/**
 * Automatische Screenshots der Demo-App und der Referenzseite.
 *
 * Verwendung:
 *   npm run screenshots              → Demo-App + Referenzseite
 *   npm run screenshots -- --demo    → nur Demo-App
 *   npm run screenshots -- --ref     → nur Referenzseite
 */

import { chromium } from "@playwright/test";
import { execSync, spawn } from "child_process";
import * as fs from "fs";
import * as path from "path";
import * as http from "http";

const DEMO_URL = "http://localhost:5174";
const REF_URL = "https://www.ergo.de";
const OUT_DIR = path.resolve(__dirname, "../screenshots");

const args = process.argv.slice(2);
const onlyDemo = args.includes("--demo");
const onlyRef = args.includes("--ref");

// ── Helpers ──────────────────────────────────────────────────────────────────

function ensureDir(dir: string) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function waitForServer(url: string, timeoutMs = 15_000): Promise<void> {
  return new Promise((resolve, reject) => {
    const start = Date.now();
    const check = () => {
      http
        .get(url, (res) => {
          if (res.statusCode && res.statusCode < 500) resolve();
          else setTimeout(check, 300);
        })
        .on("error", () => {
          if (Date.now() - start > timeoutMs) reject(new Error(`Timeout: ${url} nicht erreichbar`));
          else setTimeout(check, 300);
        });
    };
    check();
  });
}

// ── Demo-App Screenshots ──────────────────────────────────────────────────────

const DEMO_SECTIONS = [
  { name: "stepper",      selector: "section:has(h2)" ,   nth: 1  },
  { name: "button",       selector: "section:has(h2)",    nth: 2  },
  { name: "link",         selector: "section:has(h2)",    nth: 3  },
  { name: "tooltip",      selector: "section:has(h2)",    nth: 4  },
  { name: "text-input",   selector: "section:has(h2)",    nth: 5  },
  { name: "textarea",     selector: "section:has(h2)",    nth: 6  },
  { name: "select",       selector: "section:has(h2)",    nth: 7  },
  { name: "slider",       selector: "section:has(h2)",    nth: 8  },
  { name: "date-input",   selector: "section:has(h2)",    nth: 9  },
  { name: "radio-button", selector: "section:has(h2)",    nth: 10 },
  { name: "checkbox",     selector: "section:has(h2)",    nth: 11 },
  { name: "toggle",       selector: "section:has(h2)",    nth: 12 },
  { name: "modal",        selector: "section:has(h2)",    nth: 13 },
  { name: "toast",        selector: "section:has(h2)",    nth: 14 },
];

async function screenshotDemo() {
  const outDir = path.join(OUT_DIR, "demo");
  ensureDir(outDir);

  console.log("→ Warte auf Demo-Server...");
  await waitForServer(DEMO_URL);

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });

  await page.goto(DEMO_URL, { waitUntil: "networkidle" });

  // Vollseite
  await page.screenshot({ path: path.join(outDir, "full-page.png"), fullPage: true });
  console.log("  ✓ full-page.png");

  // Einzelne Sections
  const sections = await page.locator("section:has(h2)").all();
  for (let i = 0; i < sections.length; i++) {
    const info = DEMO_SECTIONS[i];
    if (!info) continue;
    await sections[i].scrollIntoViewIfNeeded();
    await sections[i].screenshot({ path: path.join(outDir, `${info.name}.png`) });
    console.log(`  ✓ ${info.name}.png`);
  }

  await browser.close();
  console.log(`\nDemo-Screenshots gespeichert in: ${outDir}\n`);
}

// ── Referenzseite Screenshots ─────────────────────────────────────────────────

const REF_PAGES = [
  {
    name: "home",
    url: REF_URL,
    clip: undefined,
  },
];

async function screenshotRef() {
  const outDir = path.join(OUT_DIR, "reference");
  ensureDir(outDir);

  const browser = await chromium.launch();

  for (const p of REF_PAGES) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    console.log(`→ ${p.url}`);
    try {
      await page.goto(p.url, { waitUntil: "domcontentloaded", timeout: 30_000 });
      await page.waitForTimeout(2000);
      await page.screenshot({
        path: path.join(outDir, `${p.name}.png`),
        fullPage: false,
      });
      console.log(`  ✓ ${p.name}.png`);
    } catch (e) {
      console.warn(`  ✗ ${p.name} fehlgeschlagen:`, (e as Error).message);
    }
    await page.close();
  }

  await browser.close();
  console.log(`\nReferenz-Screenshots gespeichert in: ${outDir}\n`);
}

// ── Main ──────────────────────────────────────────────────────────────────────

(async () => {
  ensureDir(OUT_DIR);

  if (!onlyRef) await screenshotDemo();
  if (!onlyDemo) await screenshotRef();
})();
