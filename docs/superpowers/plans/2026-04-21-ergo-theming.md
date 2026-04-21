# Themeable ERGO Content Pages — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract all hardcoded CSS values from 19 ERGO components into CSS custom properties and expand `initTheme()` to accept the full token set, enabling live theme switching for demos.

**Architecture:** Flat CSS variables in `:root` (theme.css). Components consume variables directly. `initTheme()` injects overrides via a `<style>` tag. Three preset themes ship with the library.

**Tech Stack:** CSS custom properties, TypeScript, Rollup (existing build)

**Hard constraint:** Current ERGO appearance must be pixel-identical after refactor. All new variable defaults match current hardcoded values exactly.

---

## File Structure

### Modified files
- `src/theme/theme.css` — Add 7 new color variables + 11 font-size variables to `:root`
- `src/theme/index.ts` — Expand `ThemeConfig`, rewrite `initTheme()` with full TOKEN_MAP
- `src/index.ts` — Add preset exports
- 19 CSS files in `src/components/ergo/*/` — Replace hardcoded values with `var(--token)`

### New files
- `src/theme/presets.ts` — Three preset theme objects

---

### Task 1: Expand theme.css with new tokens

**Files:**
- Modify: `src/theme/theme.css`

- [ ] **Step 1: Add new color and font-size tokens to `:root`**

In `src/theme/theme.css`, replace the entire `:root` block with:

```css
:root {
  /* ERGO brand: Weinrot #8e0038, secondary red #bf1528 */
  --color-primary: #8e0038;
  --color-secondary: #bf1528;
  --color-tertiary: #71022e;
  --color-text: #333333;
  --color-text-muted: #737373;
  --color-text-light: #aaaaaa;
  --color-text-subtle: #999999;
  --color-text-secondary: #555555;
  --color-border: #d9d9d9;
  --color-border-card: #c9c5c7;
  --color-border-light: #e5e5e5;
  --color-bg-disabled: #f2f2f2;
  --color-text-disabled: #aeaeae;
  --color-bg-white: #ffffff;
  --color-bg-warm: #fbf4f4;
  --color-bg-cream: #faf5ef;
  --border-radius: 4px;
  --border-radius-large: 8px;
  --border-radius-pill: 100px;
  --border-radius-button: 16px;
  --transition: 150ms ease;
  --font-family: "DM Sans", Arial, Helvetica, sans-serif;
  --font-family-heading: "Fedra Serif", Georgia, "Times New Roman", serif;
  --box-shadow-small: 0 4px 5px 0 rgba(0,0,0,.14), 0 1px 10px 0 rgba(0,0,0,.12), 0 2px 4px -1px rgba(0,0,0,.2);
  --box-shadow-medium: 0 3px 5px -1px rgba(0,0,0,.2), 0 6px 10px 0 rgba(0,0,0,.14), 0 1px 18px 0 rgba(0,0,0,.12);
  --color-focus: #326ec8;

  /* ERGO site section backgrounds */
  --color-bg-blue: #ccebed;
  --color-bg-green: #d3ebe5;
  --color-bg-yellow: #fef6d2;
  --color-bg-magenta: #f5e1eb;
  --color-flag: #c34a89;

  /* Font size scale */
  --font-size-xs: 11px;
  --font-size-sm: 12px;
  --font-size-base: 14px;
  --font-size-md: 15px;
  --font-size-lg: 16px;
  --font-size-xl: 18px;
  --font-size-2xl: 20px;
  --font-size-3xl: 24px;
  --font-size-4xl: 28px;
  --font-size-5xl: 32px;
  --font-size-6xl: 40px;

  /* Spacing scale */
  --space-xxs: 4px;
  --space-xs: 12px;
  --space-s: 16px;
  --space-base: 24px;
  --space-m: 32px;
  --space-l: 48px;
  --space-xl: 64px;
  --space-xxl: 96px;

  /* Layout */
  --max-width: 1440px;
}
```

- [ ] **Step 2: Verify build**

Run: `npm run build`
Expected: Success, no errors

- [ ] **Step 3: Commit**

```bash
git add src/theme/theme.css
git commit -m "feat(theme): add color and font-size tokens to theme.css"
```

---

### Task 2: Rewrite initTheme() and ThemeConfig

**Files:**
- Modify: `src/theme/index.ts`

- [ ] **Step 1: Replace src/theme/index.ts with expanded implementation**

Replace the entire file with:

```typescript
import "./theme.css";

export interface ThemeConfig {
  // Colors
  primary?: string;
  secondary?: string;
  tertiary?: string;
  text?: string;
  textMuted?: string;
  textLight?: string;
  textSubtle?: string;
  textSecondary?: string;
  border?: string;
  borderCard?: string;
  borderLight?: string;
  bgDisabled?: string;
  textDisabled?: string;
  focus?: string;
  flag?: string;
  bgWhite?: string;
  bgWarm?: string;
  bgCream?: string;
  bgBlue?: string;
  bgGreen?: string;
  bgYellow?: string;
  bgMagenta?: string;

  // Typography
  fontFamily?: string;
  fontFamilyHeading?: string;
  fontSizeXs?: string;
  fontSizeSm?: string;
  fontSizeBase?: string;
  fontSizeMd?: string;
  fontSizeLg?: string;
  fontSizeXl?: string;
  fontSize2xl?: string;
  fontSize3xl?: string;
  fontSize4xl?: string;
  fontSize5xl?: string;
  fontSize6xl?: string;

  // Spacing
  spaceXxs?: string;
  spaceXs?: string;
  spaceS?: string;
  spaceBase?: string;
  spaceM?: string;
  spaceL?: string;
  spaceXl?: string;
  spaceXxl?: string;

  // Radii
  borderRadius?: string;
  borderRadiusLarge?: string;
  borderRadiusPill?: string;
  borderRadiusButton?: string;

  // Shadows
  boxShadowSmall?: string;
  boxShadowMedium?: string;

  // Layout
  transition?: string;
  maxWidth?: string;
}

const TOKEN_MAP: Record<keyof ThemeConfig, string> = {
  primary: "--color-primary",
  secondary: "--color-secondary",
  tertiary: "--color-tertiary",
  text: "--color-text",
  textMuted: "--color-text-muted",
  textLight: "--color-text-light",
  textSubtle: "--color-text-subtle",
  textSecondary: "--color-text-secondary",
  border: "--color-border",
  borderCard: "--color-border-card",
  borderLight: "--color-border-light",
  bgDisabled: "--color-bg-disabled",
  textDisabled: "--color-text-disabled",
  focus: "--color-focus",
  flag: "--color-flag",
  bgWhite: "--color-bg-white",
  bgWarm: "--color-bg-warm",
  bgCream: "--color-bg-cream",
  bgBlue: "--color-bg-blue",
  bgGreen: "--color-bg-green",
  bgYellow: "--color-bg-yellow",
  bgMagenta: "--color-bg-magenta",
  fontFamily: "--font-family",
  fontFamilyHeading: "--font-family-heading",
  fontSizeXs: "--font-size-xs",
  fontSizeSm: "--font-size-sm",
  fontSizeBase: "--font-size-base",
  fontSizeMd: "--font-size-md",
  fontSizeLg: "--font-size-lg",
  fontSizeXl: "--font-size-xl",
  fontSize2xl: "--font-size-2xl",
  fontSize3xl: "--font-size-3xl",
  fontSize4xl: "--font-size-4xl",
  fontSize5xl: "--font-size-5xl",
  fontSize6xl: "--font-size-6xl",
  spaceXxs: "--space-xxs",
  spaceXs: "--space-xs",
  spaceS: "--space-s",
  spaceBase: "--space-base",
  spaceM: "--space-m",
  spaceL: "--space-l",
  spaceXl: "--space-xl",
  spaceXxl: "--space-xxl",
  borderRadius: "--border-radius",
  borderRadiusLarge: "--border-radius-large",
  borderRadiusPill: "--border-radius-pill",
  borderRadiusButton: "--border-radius-button",
  boxShadowSmall: "--box-shadow-small",
  boxShadowMedium: "--box-shadow-medium",
  transition: "--transition",
  maxWidth: "--max-width",
};

export function initTheme(config: ThemeConfig = {}): void {
  const id = "demo-ui-lib-theme";
  let el = document.getElementById(id) as HTMLStyleElement | null;

  const entries = Object.entries(config)
    .filter(([_, v]) => v !== undefined)
    .map(([k, v]) => `${TOKEN_MAP[k as keyof ThemeConfig]}:${v}`);

  if (entries.length === 0) {
    el?.remove();
    return;
  }

  const css = `:root{${entries.join(";")}}`;
  if (!el) {
    el = document.createElement("style");
    el.id = id;
    document.head.appendChild(el);
  }
  el.textContent = css;
}
```

- [ ] **Step 2: Verify build**

Run: `npm run build`
Expected: Success, no errors

- [ ] **Step 3: Commit**

```bash
git add src/theme/index.ts
git commit -m "feat(theme): expand initTheme to accept full token set"
```

---

### Task 3: Add theme presets

**Files:**
- Create: `src/theme/presets.ts`
- Modify: `src/index.ts`

- [ ] **Step 1: Create src/theme/presets.ts**

```typescript
import type { ThemeConfig } from "./index";

export const ergoTheme: ThemeConfig = {};

export const modernBlueTheme: ThemeConfig = {
  primary: "#1a56db",
  secondary: "#2563eb",
  tertiary: "#1e40af",
  focus: "#3b82f6",
  flag: "#6366f1",
  bgWarm: "#eff6ff",
  bgCream: "#f0f5ff",
  bgBlue: "#dbeafe",
  bgGreen: "#d1fae5",
  bgYellow: "#fef3c7",
  bgMagenta: "#e0e7ff",
  fontFamily: '"Inter", "DM Sans", Arial, Helvetica, sans-serif',
  fontFamilyHeading: '"Inter", "DM Sans", Arial, Helvetica, sans-serif',
};

export const warmNeutralTheme: ThemeConfig = {
  primary: "#78716c",
  secondary: "#a8a29e",
  tertiary: "#57534e",
  focus: "#92400e",
  flag: "#b45309",
  bgWarm: "#faf5f0",
  bgCream: "#faf5ef",
  bgBlue: "#f5f0eb",
  bgGreen: "#f0ebe5",
  bgYellow: "#faf5e5",
  bgMagenta: "#f5ebe5",
  fontFamily: '"Source Sans 3", "DM Sans", Arial, Helvetica, sans-serif',
  fontFamilyHeading: '"Playfair Display", Georgia, "Times New Roman", serif',
};
```

- [ ] **Step 2: Add preset exports to src/index.ts**

Add these lines at the end of `src/index.ts`, after the ErgoFooter exports:

```typescript
export { ergoTheme, modernBlueTheme, warmNeutralTheme } from "./theme/presets";
```

- [ ] **Step 3: Verify build**

Run: `npm run build`
Expected: Success, no errors

- [ ] **Step 4: Commit**

```bash
git add src/theme/presets.ts src/index.ts
git commit -m "feat(theme): add ergo, modernBlue, warmNeutral theme presets"
```

---

### Task 4: Tokenize ErgoCtaButton CSS

**Files:**
- Modify: `src/components/ergo/ErgoCtaButton/ErgoCtaButton.css`

- [ ] **Step 1: Replace hardcoded values**

Make these replacements in `ErgoCtaButton.css`:

| Line | Old | New |
|------|-----|-----|
| 6 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 25 | `color: #ffffff;` | `color: var(--color-bg-white);` |
| 59 | `color: #ffffff;` | `color: var(--color-bg-white);` |

- [ ] **Step 2: Verify build**

Run: `npm run build`
Expected: Success

- [ ] **Step 3: Commit**

```bash
git add src/components/ergo/ErgoCtaButton/ErgoCtaButton.css
git commit -m "refactor(ergo): tokenize ErgoCtaButton CSS"
```

---

### Task 5: Tokenize ErgoPriceDisplay CSS

**Files:**
- Modify: `src/components/ergo/ErgoPriceDisplay/ErgoPriceDisplay.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 4 | `gap: 4px;` | `gap: var(--space-xxs);` |
| 10 | `font-size: 14px;` | `font-size: var(--font-size-base);` |
| 24 | `font-size: 14px;` | `font-size: var(--font-size-base);` |
| 30 | `font-size: 40px;` | `font-size: var(--font-size-6xl);` |
| 34 | `font-size: 24px;` | `font-size: var(--font-size-3xl);` |
| 39 | `font-size: 28px;` | `font-size: var(--font-size-4xl);` |
| 43 | `font-size: 18px;` | `font-size: var(--font-size-xl);` |
| 48 | `font-size: 20px;` | `font-size: var(--font-size-2xl);` |
| 52 | `font-size: 14px;` | `font-size: var(--font-size-base);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoPriceDisplay/ErgoPriceDisplay.css && git commit -m "refactor(ergo): tokenize ErgoPriceDisplay CSS"
```

---

### Task 6: Tokenize ErgoPromoFlag CSS

**Files:**
- Modify: `src/components/ergo/ErgoPromoFlag/ErgoPromoFlag.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 4 | `color: #ffffff;` | `color: var(--color-bg-white);` |
| 6 | `font-size: 14px;` | `font-size: var(--font-size-base);` |
| 8 | `padding: 6px 12px;` | `padding: 6px var(--space-xs);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoPromoFlag/ErgoPromoFlag.css && git commit -m "refactor(ergo): tokenize ErgoPromoFlag CSS"
```

---

### Task 7: Tokenize ErgoAccordion CSS

**Files:**
- Modify: `src/components/ergo/ErgoAccordion/ErgoAccordion.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 19 | `gap: 16px;` | `gap: var(--space-s);` |
| 35 | `font-size: 18px;` | `font-size: var(--font-size-xl);` |
| 70 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 73 | `margin: 0 0 12px;` | `margin: 0 0 var(--space-xs);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoAccordion/ErgoAccordion.css && git commit -m "refactor(ergo): tokenize ErgoAccordion CSS"
```

---

### Task 8: Tokenize ErgoArticleTeaser CSS

**Files:**
- Modify: `src/components/ergo/ErgoArticleTeaser/ErgoArticleTeaser.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 7 | `gap: 12px;` | `gap: var(--space-xs);` |
| 13 | `font-size: 24px;` | `font-size: var(--font-size-3xl);` |
| 21 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 28 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoArticleTeaser/ErgoArticleTeaser.css && git commit -m "refactor(ergo): tokenize ErgoArticleTeaser CSS"
```

---

### Task 9: Tokenize ErgoPromoBanner CSS

**Files:**
- Modify: `src/components/ergo/ErgoPromoBanner/ErgoPromoBanner.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 13 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoPromoBanner/ErgoPromoBanner.css && git commit -m "refactor(ergo): tokenize ErgoPromoBanner CSS"
```

---

### Task 10: Tokenize ErgoStickyFooter CSS

**Files:**
- Modify: `src/components/ergo/ErgoStickyFooter/ErgoStickyFooter.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 7 | `background-color: #ffffff;` | `background-color: var(--color-bg-white);` |
| 35 | `font-size: 18px;` | `font-size: var(--font-size-xl);` |
| 41 | `font-size: 14px;` | `font-size: var(--font-size-base);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoStickyFooter/ErgoStickyFooter.css && git commit -m "refactor(ergo): tokenize ErgoStickyFooter CSS"
```

---

### Task 11: Tokenize ErgoExpansionPanel CSS

**Files:**
- Modify: `src/components/ergo/ErgoExpansionPanel/ErgoExpansionPanel.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 13 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 49 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoExpansionPanel/ErgoExpansionPanel.css && git commit -m "refactor(ergo): tokenize ErgoExpansionPanel CSS"
```

---

### Task 12: Tokenize ErgoReviewSection CSS

**Files:**
- Modify: `src/components/ergo/ErgoReviewSection/ErgoReviewSection.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 11 | `font-size: 20px;` | `font-size: var(--font-size-2xl);` |
| 32 | `gap: 12px;` | `gap: var(--space-xs);` |
| 42 | `font-size: 24px;` | `font-size: var(--font-size-3xl);` |
| 48 | `font-size: 14px;` | `font-size: var(--font-size-base);` |
| 50 | `margin-bottom: 4px;` | `margin-bottom: var(--space-xxs);` |
| 54 | `font-size: 14px;` | `font-size: var(--font-size-base);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoReviewSection/ErgoReviewSection.css && git commit -m "refactor(ergo): tokenize ErgoReviewSection CSS"
```

---

### Task 13: Tokenize ErgoDownloadLink CSS

**Files:**
- Modify: `src/components/ergo/ErgoDownloadLink/ErgoDownloadLink.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 36 | `font-size: 14px;` | `font-size: var(--font-size-base);` |
| 42 | `font-size: 12px;` | `font-size: var(--font-size-sm);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoDownloadLink/ErgoDownloadLink.css && git commit -m "refactor(ergo): tokenize ErgoDownloadLink CSS"
```

---

### Task 14: Tokenize ErgoCompanyLogos CSS

**Files:**
- Modify: `src/components/ergo/ErgoCompanyLogos/ErgoCompanyLogos.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 11 | `height: 48px;` | `height: var(--space-l);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoCompanyLogos/ErgoCompanyLogos.css && git commit -m "refactor(ergo): tokenize ErgoCompanyLogos CSS"
```

---

### Task 15: Tokenize ErgoHeader CSS

**Files:**
- Modify: `src/components/ergo/ErgoHeader/ErgoHeader.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 7 | `background-color: #ffffff;` | `background-color: var(--color-bg-white);` |
| 35 | `font-size: 11px;` | `font-size: var(--font-size-xs);` |
| 44 | `gap: 4px;` | `gap: var(--space-xxs);` |
| 51 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 56 | `padding: 12px 16px;` | `padding: var(--space-xs) var(--space-s);` |
| 65 | `background-color: #fbf4f4;` | `background-color: var(--color-bg-warm);` |
| 70 | `background-color: #fbf4f4;` | `background-color: var(--color-bg-warm);` |
| 77 | `gap: 4px;` | `gap: var(--space-xxs);` |
| 93 | `font-size: 12px;` | `font-size: var(--font-size-sm);` |
| 99 | `background-color: #fbf4f4;` | `background-color: var(--color-bg-warm);` |
| 120 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 126 | `font-size: 11px;` | `font-size: var(--font-size-xs);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoHeader/ErgoHeader.css && git commit -m "refactor(ergo): tokenize ErgoHeader CSS"
```

---

### Task 16: Tokenize ErgoMegaMenu CSS

**Files:**
- Modify: `src/components/ergo/ErgoMegaMenu/ErgoMegaMenu.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 6 | `background: #ffffff;` | `background: var(--color-bg-white);` |
| 29 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 42 | `font-size: 14px;` | `font-size: var(--font-size-base);` |
| 70 | `padding: 12px 16px;` | `padding: var(--space-xs) var(--space-s);` |
| 76 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 83 | `background-color: #fbf4f4;` | `background-color: var(--color-bg-warm);` |
| 105 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 121 | `gap: 12px;` | `gap: var(--space-xs);` |
| 125 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 131 | `font-size: 14px;` | `font-size: var(--font-size-base);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoMegaMenu/ErgoMegaMenu.css && git commit -m "refactor(ergo): tokenize ErgoMegaMenu CSS"
```

---

### Task 17: Tokenize ErgoFooter CSS

**Files:**
- Modify: `src/components/ergo/ErgoFooter/ErgoFooter.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 21 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 37 | `font-size: 14px;` | `font-size: var(--font-size-base);` |
| 56 | `font-size: 14px;` | `font-size: var(--font-size-base);` |
| 62 | `gap: 16px;` | `gap: var(--space-s);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoFooter/ErgoFooter.css && git commit -m "refactor(ergo): tokenize ErgoFooter CSS"
```

---

### Task 18: Tokenize ErgoPromoCard CSS

**Files:**
- Modify: `src/components/ergo/ErgoPromoCard/ErgoPromoCard.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 2 | `background-color: #ffffff;` | `background-color: var(--color-bg-white);` |
| 52 | `bottom: 12px;` | `bottom: var(--space-xs);` |
| 53 | `right: 12px;` | `right: var(--space-xs);` |
| 61 | `right: 16px;` | `right: var(--space-s);` |
| 69 | `gap: 12px;` | `gap: var(--space-xs);` |
| 74 | `font-size: 18px;` | `font-size: var(--font-size-xl);` |
| 82 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 90 | `margin: 4px 0;` | `margin: var(--space-xxs) 0;` |
| 96 | `gap: 12px;` | `gap: var(--space-xs);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoPromoCard/ErgoPromoCard.css && git commit -m "refactor(ergo): tokenize ErgoPromoCard CSS"
```

---

### Task 19: Tokenize ErgoCarousel CSS

**Files:**
- Modify: `src/components/ergo/ErgoCarousel/ErgoCarousel.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 51 | `gap: 12px;` | `gap: var(--space-xs);` |
| 63 | `background: #ffffff;` | `background: var(--color-bg-white);` |
| 95 | `background: #d9d9d9;` | `background: var(--color-border);` |
| 107 | `background: #aaaaaa;` | `background: var(--color-text-light);` |

Note: `#d9d9d9` in the carousel dots maps to `--color-border` (same value already in theme.css). The carousel `--carousel-gap, 24px` defaults already use CSS variable fallbacks — leave those as-is.

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoCarousel/ErgoCarousel.css && git commit -m "refactor(ergo): tokenize ErgoCarousel CSS"
```

---

### Task 20: Tokenize ErgoSectionHeader CSS

**Files:**
- Modify: `src/components/ergo/ErgoSectionHeader/ErgoSectionHeader.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 8 | `font-size: 18px;` | `font-size: var(--font-size-xl);` |
| 18 | `font-size: 28px;` | `font-size: var(--font-size-4xl);` |
| 22 | `margin: 0 0 12px;` | `margin: 0 0 var(--space-xs);` |
| 31 | `font-size: 18px;` | `font-size: var(--font-size-xl);` |
| 40 | `font-size: 24px;` | `font-size: var(--font-size-3xl);` |
| 44 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 48 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoSectionHeader/ErgoSectionHeader.css && git commit -m "refactor(ergo): tokenize ErgoSectionHeader CSS"
```

---

### Task 21: Tokenize ErgoTileCard CSS

**Files:**
- Modify: `src/components/ergo/ErgoTileCard/ErgoTileCard.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 9 | `gap: 12px;` | `gap: var(--space-xs);` |
| 22 | `height: 48px;` | `height: var(--space-l);` |
| 26 | `height: 48px;` | `height: var(--space-l);` |
| 31 | `font-size: 28px;` | `font-size: var(--font-size-4xl);` |
| 38 | `font-size: 18px;` | `font-size: var(--font-size-xl);` |
| 45 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 56 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 75 | `background: #ffffff;` | `background: var(--color-bg-white);` |
| 76 | `border: 1px solid #e5e5e5;` | `border: 1px solid var(--color-border-light);` |
| 85 | `gap: 12px;` | `gap: var(--space-xs);` |
| 86 | `padding: 16px 20px;` | `padding: var(--space-s) 20px;` |
| 105 | `font-size: 15px;` | `font-size: var(--font-size-md);` |
| 113 | `font-size: 14px;` | `font-size: var(--font-size-base);` |
| 135 | `background: #fff;` | `background: var(--color-bg-white);` |
| 136 | `border: 1px solid #e5e5e5;` | `border: 1px solid var(--color-border-light);` |
| 148 | `border-color: #999;` | `border-color: var(--color-text-subtle);` |
| 152 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 156 | `font-size: 15px;` | `font-size: var(--font-size-md);` |
| 157 | `color: #555;` | `color: var(--color-text-secondary);` |
| 161 | `margin-top: 12px;` | `margin-top: var(--space-xs);` |
| 166 | `background-color: #ffffff;` | `background-color: var(--color-bg-white);` |
| 177 | `margin-top: 12px;` | `margin-top: var(--space-xs);` |
| 182 | `color: #ffffff;` | `color: var(--color-bg-white);` |
| 192 | `background-color: #ffffff;` | `background-color: var(--color-bg-white);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoTileCard/ErgoTileCard.css && git commit -m "refactor(ergo): tokenize ErgoTileCard CSS"
```

---

### Task 22: Tokenize ErgoHeroBanner CSS

**Files:**
- Modify: `src/components/ergo/ErgoHeroBanner/ErgoHeroBanner.css`

- [ ] **Step 1: Replace hardcoded values**

| Line | Old | New |
|------|-----|-----|
| 61 | `gap: 12px;` | `gap: var(--space-xs);` |
| 65 | `background-color: #faf5ef;` | `background-color: var(--color-bg-cream);` |
| 69 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 77 | `font-size: 32px;` | `font-size: var(--font-size-5xl);` |
| 85 | `font-size: 16px;` | `font-size: var(--font-size-lg);` |
| 98 | `gap: 12px;` | `gap: var(--space-xs);` |
| 104 | `top: 24px;` | `top: var(--space-base);` |
| 105 | `right: 24px;` | `right: var(--space-base);` |
| 106 | `width: 96px;` | `width: var(--space-xxl);` |
| 107 | `height: 96px;` | `height: var(--space-xxl);` |
| 135 | `font-size: 24px;` | `font-size: var(--font-size-3xl);` |
| 139 | `width: 64px;` | `width: var(--space-xl);` |
| 140 | `height: 64px;` | `height: var(--space-xl);` |
| 141 | `top: 12px;` | `top: var(--space-xs);` |
| 142 | `right: 12px;` | `right: var(--space-xs);` |

- [ ] **Step 2: Verify build, commit**

```bash
npm run build && git add src/components/ergo/ErgoHeroBanner/ErgoHeroBanner.css && git commit -m "refactor(ergo): tokenize ErgoHeroBanner CSS"
```

---

### Task 23: Final verification

- [ ] **Step 1: Full build**

Run: `npm run build`
Expected: Success with no errors or warnings

- [ ] **Step 2: Run tests**

Run: `npm test`
Expected: All tests pass

- [ ] **Step 3: Visual check**

Run: `npm run demo:ergo`

Open the demo in browser. Verify the ERGO pages look pixel-identical to before:
- Check header, footer, hero banner, promo cards, tile cards, carousel, accordion, section headers
- All colors, fonts, spacing should be exactly the same as before the refactor

- [ ] **Step 4: Test theme switching**

Open browser console on the demo page and run:

```javascript
// Import is already loaded — access via window or module
// In the demo app, add a quick test:
import { initTheme, modernBlueTheme } from 'demo-ui-lib';

initTheme(modernBlueTheme);
// Verify: page updates to blue theme — primary color, backgrounds, fonts change

initTheme({ primary: '#0d9488' });
// Verify: only primary color changes to teal

initTheme();
// Verify: resets back to ERGO defaults
```

- [ ] **Step 5: Final commit if any adjustments were needed**

```bash
git add -A && git commit -m "fix: address visual regression issues from theme tokenization"
```

Only run this if Step 3 or 4 revealed issues that needed fixing.
