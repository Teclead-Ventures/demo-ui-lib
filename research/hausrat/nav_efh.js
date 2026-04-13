async function run(page) {
  // Step 1: Select Einfamilienhaus (second button) and click weiter
  await page.waitForTimeout(2000);
  const buttons1 = await page.locator("main button").all();
  await buttons1[1].click();
  await page.waitForTimeout(1000);
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(3000);

  // For EFH, step 2 might be different (no floor selection)
  // Check if we're on m2 or home-location
  const url1 = page.url();
  if (url1.includes('home-location')) {
    // Still have floor selection for EFH? Select ground floor equivalent
    const buttons2 = await page.locator("main button").all();
    await buttons2[0].click();
    await page.waitForTimeout(1000);
    await page.getByTestId("submit-button").click();
    await page.waitForTimeout(3000);
  }

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
}
