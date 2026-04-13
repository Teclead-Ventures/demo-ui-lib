// Collect Rechtsschutz prices across ages
// Run: playwright-cli -s=rechtsschutz run-code "$(cat research/rechtsschutz/collect_prices.js)"
// NOTE: This must be run from the configurator page (step 5)

// Helper to read price after delay
async function getPrice() {
  await page.waitForTimeout(3000);
  const text = await page.evaluate(() => {
    const el = document.querySelector("[class*=price], [class*=beitrag], [class*=Price]");
    return el ? el.textContent : "not found";
  });
  const match = text.match(/([\d,.]+)\s*€/);
  return match ? parseFloat(match[1].replace(",", ".")) : null;
}

const price = await getPrice();
console.log("Current price:", price);
