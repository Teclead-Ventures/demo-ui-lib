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

  // Step 3: Enter 80 m2
  await page.getByTestId("inputSizeHome").fill("80");
  await page.waitForTimeout(1000);
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(3000);

  // Step 4: Address
  await page.getByTestId("street-name-input").fill("Altmarkt");
  await page.getByTestId("street-number-input").fill("12");
  await page.getByTestId("zip-code-input").fill("01067");
  await page.waitForTimeout(3000);
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(3000);

  // Step 5: Insurance start (default)
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(3000);

  // Step 6: Birth date
  await page.getByRole("spinbutton", {name: "Tag"}).fill("15");
  await page.getByRole("spinbutton", {name: "Monat"}).fill("03");
  await page.getByRole("spinbutton", {name: "Jahr"}).fill("1990");
  await page.waitForTimeout(1000);
  await page.getByTestId("submit-button").click();
  await page.waitForTimeout(5000);
}
