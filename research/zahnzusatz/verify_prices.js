async page => {
  const results = [];

  // Test ages at boundaries and within bands
  const tests = [
    { year: 2001, age: 25, expected: 9.20,  band: "21-25" },
    { year: 1997, age: 29, expected: 17.50, band: "26-30" },
    { year: 1991, age: 35, expected: 27.60, band: "31-40" },
    { year: 1984, age: 42, expected: 41.30, band: "41-50" },
    { year: 1978, age: 48, expected: 41.30, band: "41-50" },
    { year: 1966, age: 60, expected: 57.80, band: "51+" },
  ];

  for (let i = 0; i < tests.length; i++) {
    const t = tests[i];
    await page.goto('https://www.ergo.de/de/Produkte/Zahnzusatzversicherung/zahnersatz/abschluss_DS100');
    await page.waitForTimeout(2000);

    // Dismiss cookies on first run
    if (i === 0) {
      try {
        const btn = page.getByRole('button', { name: 'Alle akzeptieren' });
        if (await btn.isVisible({ timeout: 2000 })) await btn.click();
        await page.waitForTimeout(1000);
      } catch(e) {}
    }

    // Step 1: Select Ich + weiter
    await page.locator('label').filter({ hasText: /^Ich$/ }).click();
    await page.waitForTimeout(300);
    await page.getByRole('button', { name: 'weiter' }).click();
    await page.waitForTimeout(1500);

    // Step 2: Enter birth date + weiter
    await page.getByRole('spinbutton', { name: 'Tag' }).fill('15');
    await page.getByRole('spinbutton', { name: 'Monat' }).fill('03');
    await page.getByRole('spinbutton', { name: 'Jahr' }).fill(String(t.year));
    await page.waitForTimeout(1000);
    await page.getByRole('button', { name: 'weiter' }).click();
    await page.waitForTimeout(2000);

    // Extract price from the calculator app
    const text = await page.locator('#ppzApp').textContent();
    const match = text.match(/Ab dem 7\. Monat je\s*([\d,.]+)\s*€/);
    const actual = match ? parseFloat(match[1].replace('.', '').replace(',', '.')) : null;

    results.push({
      age: t.age,
      band: t.band,
      expected: t.expected,
      actual: actual,
      match: actual === t.expected
    });

    await page.waitForTimeout(3000);
  }

  return JSON.stringify(results, null, 2);
}
