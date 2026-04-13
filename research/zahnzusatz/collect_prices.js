async page => {
  async function collectPrice(page, tariff, birthYear, isFirstRun) {
    const url = `https://www.ergo.de/de/Produkte/Zahnzusatzversicherung/zahnersatz/abschluss_${tariff}`;

    // Navigate fresh
    await page.goto(url);
    await page.waitForTimeout(3000);

    // Dismiss cookie banner on first run
    if (isFirstRun) {
      try {
        const cookieBtn = page.getByRole('button', { name: 'Alle akzeptieren' });
        if (await cookieBtn.isVisible({ timeout: 2000 })) {
          await cookieBtn.click();
          await page.waitForTimeout(1000);
        }
      } catch (e) {}
    }

    // Step 1: Select "Ich" and click weiter
    await page.locator('label').filter({ hasText: /^Ich$/ }).click();
    await page.waitForTimeout(500);
    await page.getByRole('button', { name: 'weiter' }).click();
    await page.waitForTimeout(2000);

    // Step 2: Enter birth date
    await page.getByRole('spinbutton', { name: 'Tag' }).fill('15');
    await page.getByRole('spinbutton', { name: 'Monat' }).fill('03');
    await page.getByRole('spinbutton', { name: 'Jahr' }).fill(String(birthYear));
    await page.waitForTimeout(1000);

    // Step 3: Click weiter to ADVANCE PAST birth date to see price
    await page.getByRole('button', { name: 'weiter' }).click();
    await page.waitForTimeout(2000);

    // Now on insurance-beginning page — extract price
    const pageText = await page.locator('main').textContent();

    const fullPriceMatch = pageText.match(/Ab dem 7\. Monat je\s*([\d,.]+)\s*€/);
    const halfPriceMatch = pageText.match(/([\d,.]+)\s*€\s*monatlich/);

    const fullPrice = fullPriceMatch ? parseFloat(fullPriceMatch[1].replace('.', '').replace(',', '.')) : null;
    const halfPrice = halfPriceMatch ? parseFloat(halfPriceMatch[1].replace('.', '').replace(',', '.')) : null;

    const age = 2026 - birthYear;
    return { tariff, birthYear, age, halfPrice, fullPrice };
  }

  const tariffs = ['DS75', 'DS90', 'DS100'];
  const birthYears = [
    2006, // age 20
    2004, // age 22
    2001, // age 25
    1996, // age 30
    1993, // age 33
    1991, // age 35
    1988, // age 38
    1986, // age 40
    1983, // age 43
    1981, // age 45
    1978, // age 48
    1976, // age 50
    1973, // age 53
    1971, // age 55
    1966, // age 60
    1961, // age 65
    1956, // age 70
  ];

  const results = [];
  const errors = [];
  let isFirstRun = true;

  for (const tariff of tariffs) {
    for (const birthYear of birthYears) {
      const age = 2026 - birthYear;
      try {
        const result = await collectPrice(page, tariff, birthYear, isFirstRun);
        results.push(result);
        isFirstRun = false;
        console.log(`OK: ${tariff} age ${result.age}: half=${result.halfPrice} full=${result.fullPrice}`);
      } catch (err) {
        console.log(`FAIL: ${tariff} age ${age}: ${err.message.substring(0, 100)}`);
        errors.push({ tariff, birthYear, age, error: err.message.substring(0, 200) });
      }
      // Rate limiting
      await page.waitForTimeout(5000);
    }
  }

  const output = {
    product: "zahnzusatz",
    sampled_at: "2026-04-12",
    source_url: "https://www.ergo.de/de/Produkte/Zahnzusatzversicherung/zahnersatz",
    ergo_tier_names: {
      tier1: "Dental-Schutz 75",
      tier2: "Dental-Schutz 90",
      tier3: "Dental-Schutz 100"
    },
    tier_mapping: {
      DS75: "grundschutz",
      DS90: "komfort",
      DS100: "premium"
    },
    beitragstabelle: {
      note: "Official ERGO Beitragstabelle from product page (age bands, monthly full rate after 6 months)",
      bands: [
        { age_band: "0-20",  DS75: 2.90,  DS90: 3.70,  DS100: 4.80  },
        { age_band: "21-25", DS75: 5.70,  DS90: 7.20,  DS100: 9.20  },
        { age_band: "26-30", DS75: 10.90, DS90: 13.80, DS100: 17.50 },
        { age_band: "31-40", DS75: 17.40, DS90: 21.70, DS100: 27.60 },
        { age_band: "41-50", DS75: 25.90, DS90: 32.50, DS100: 41.30 },
        { age_band: "51+",   DS75: 34.80, DS90: 44.40, DS100: 57.80 }
      ]
    },
    note: "ERGO uses age bands with flat rates per band. First 6 months at 50% (Startbeitrag). No coverage amount selection - tariff name (DS75/DS90/DS100) determines reimbursement percentage.",
    data_points: results.map(r => ({
      inputs: {
        age: r.age,
        tier: r.tariff,
        coverage: null,
        risk_class: null,
        payment_mode: "monthly"
      },
      output: {
        monthly_price: r.fullPrice,
        half_price_first_6_months: r.halfPrice,
        additional_notes: "First 6 months at 50%"
      }
    })),
    errors: errors
  };

  return JSON.stringify(output, null, 2);
}
