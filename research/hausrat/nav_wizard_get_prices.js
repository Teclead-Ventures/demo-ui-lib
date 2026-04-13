async function run(page) {
  // Step 1: Select Mehrfamilienhaus and click weiter
  await page.waitForTimeout(2000);
  const buttons1 = await page.locator("main button").all();
  await buttons1[0].click();
  await page.waitForTimeout(1000);
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(3000);

  // Step 2: Select 2. Obergeschoss and click weiter
  const buttons2 = await page.locator("main button").all();
  await buttons2[3].click();
  await page.waitForTimeout(1000);
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(3000);

  // Step 3: Enter M2_VALUE m2
  await page.getByTestId("inputSizeHome").fill("M2_VALUE");
  await page.waitForTimeout(1000);
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(3000);

  // Step 4: Address
  await page.getByTestId("street-name-input").fill("STREET_VALUE");
  await page.getByTestId("street-number-input").fill("12");
  await page.getByTestId("zip-code-input").fill("ZIP_VALUE");
  await page.waitForTimeout(3000);
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(3000);

  // Step 5: Insurance start (default)
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(3000);

  // Step 6: Birth date
  await page.getByRole("spinbutton", {name: "Tag"}).fill("15");
  await page.getByRole("spinbutton", {name: "Monat"}).fill("03");
  await page.getByRole("spinbutton", {name: "Jahr"}).fill("YEAR_VALUE");
  await page.waitForTimeout(1000);
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(5000);

  // Step 7: Read Best price (default)
  const bestBanner = await page.locator('[data-testid="banner"]').textContent();

  // Get price from the header area
  const priceArea = page.locator('main').locator('h6').locator('..').locator('..');
  const priceText = await priceArea.locator('div').nth(1).locator('div').first().textContent();

  // Switch to Smart
  await page.getByRole("tab", {name: "Smart"}).click();
  await page.waitForTimeout(3000);
  const smartPriceText = await priceArea.locator('div').nth(1).locator('div').first().textContent();

  console.log(`PRICES: Smart=${smartPriceText} Best=${priceText}`);
}
