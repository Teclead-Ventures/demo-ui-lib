async page => {
  const results = [];
  const tariffs = [
    { id: 'DS75', name: 'Dental-Schutz 75', expected_35: 17.40 },
    { id: 'DS90', name: 'Dental-Schutz 90', expected_35: 21.70 },
    { id: 'DS100', name: 'Dental-Schutz 100', expected_35: 27.60 },
  ];

  for (let i = 0; i < tariffs.length; i++) {
    const t = tariffs[i];
    const url = `https://www.ergo.de/de/Produkte/Zahnzusatzversicherung/zahnersatz/abschluss_${t.id}`;

    await page.goto(url);
    await page.waitForTimeout(2000);

    if (i === 0) {
      try {
        const btn = page.getByRole('button', { name: 'Alle akzeptieren' });
        if (await btn.isVisible({ timeout: 2000 })) await btn.click();
        await page.waitForTimeout(1000);
      } catch(e) {}
    }

    await page.locator('label').filter({ hasText: /^Ich$/ }).click();
    await page.waitForTimeout(300);
    await page.getByRole('button', { name: 'weiter' }).click();
    await page.waitForTimeout(1500);

    await page.getByRole('spinbutton', { name: 'Tag' }).fill('15');
    await page.getByRole('spinbutton', { name: 'Monat' }).fill('03');
    await page.getByRole('spinbutton', { name: 'Jahr' }).fill('1991');
    await page.waitForTimeout(1000);
    await page.getByRole('button', { name: 'weiter' }).click();
    await page.waitForTimeout(2000);

    const text = await page.locator('#ppzApp').textContent();
    const match = text.match(/Ab dem 7\. Monat je\s*([\d,.]+)\s*€/);
    const actual = match ? parseFloat(match[1].replace('.', '').replace(',', '.')) : null;

    results.push({
      tariff: t.id,
      name: t.name,
      age: 35,
      expected: t.expected_35,
      actual: actual,
      match: actual === t.expected_35
    });

    await page.waitForTimeout(3000);
  }

  return JSON.stringify(results, null, 2);
}
