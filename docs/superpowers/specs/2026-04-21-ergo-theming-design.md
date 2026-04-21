# Themeable ERGO Content Pages — Design Spec

## Goal

Make the 19 ERGO content page components in `src/components/ergo/` driven by CSS custom properties so the entire visual appearance can be swapped at runtime. This enables live demo presentations where the presenter tells Claude to change the brand and the pages update instantly via dev server hot-reload.

**Hard constraint:** The current ERGO visual appearance must be preserved exactly. Every new CSS variable defaults to the current hardcoded value. Before/after must be pixel-identical.

## Architecture: Flat CSS Variables

Single layer of ~45 CSS custom properties defined in `src/theme/theme.css` under `:root`. Components reference these variables directly — no semantic/primitive indirection.

### Token Map

#### Colors (20 total)

**Existing (13) — already in theme.css:**

| Variable | Default | Usage |
|---|---|---|
| `--color-primary` | `#8e0038` | Brand weinrot |
| `--color-secondary` | `#bf1528` | Secondary red |
| `--color-tertiary` | `#71022e` | Dark brand variant |
| `--color-text` | `#333333` | Body text |
| `--color-text-muted` | `#737373` | Muted text |
| `--color-border` | `#d9d9d9` | Standard borders |
| `--color-border-card` | `#c9c5c7` | Card borders |
| `--color-bg-disabled` | `#f2f2f2` | Disabled backgrounds |
| `--color-text-disabled` | `#aeaeae` | Disabled text |
| `--color-focus` | `#326ec8` | Focus rings |
| `--color-flag` | `#c34a89` | Promo flag |
| `--color-bg-blue` | `#ccebed` | Blue section bg |
| `--color-bg-green` | `#d3ebe5` | Green section bg |
| `--color-bg-yellow` | `#fef6d2` | Yellow section bg |
| `--color-bg-magenta` | `#f5e1eb` | Magenta section bg |

**New (7) — extracted from hardcoded values:**

| Variable | Default | Replaces | Used in |
|---|---|---|---|
| `--color-bg-white` | `#ffffff` | `#ffffff` | ErgoCtaButton, ErgoPromoFlag, ErgoStickyFooter, ErgoHeader, ErgoMegaMenu, ErgoPromoCard, ErgoCarousel, ErgoTileCard |
| `--color-bg-warm` | `#fbf4f4` | `#fbf4f4` | ErgoHeader (hover/active), ErgoMegaMenu |
| `--color-bg-cream` | `#faf5ef` | `#faf5ef` | ErgoHeroBanner |
| `--color-border-light` | `#e5e5e5` | `#e5e5e5` | ErgoTileCard |
| `--color-text-light` | `#aaaaaa` | `#aaaaaa` | ErgoCarousel (dots) |
| `--color-text-subtle` | `#999999` | `#999` | ErgoTileCard |
| `--color-text-secondary` | `#555555` | `#555` | ErgoTileCard |

#### Typography (13 total)

**Existing (2):**

| Variable | Default |
|---|---|
| `--font-family` | `"DM Sans", Arial, Helvetica, sans-serif` |
| `--font-family-heading` | `"Fedra Serif", Georgia, "Times New Roman", serif` |

**New (11) — font size scale:**

| Variable | Default | Replaces |
|---|---|---|
| `--font-size-xs` | `11px` | Header nav small, labels |
| `--font-size-sm` | `12px` | Header links, download meta |
| `--font-size-base` | `14px` | Body text, footer, prices |
| `--font-size-md` | `15px` | Tile descriptions |
| `--font-size-lg` | `16px` | Buttons, menus, body text |
| `--font-size-xl` | `18px` | Section titles, card headings |
| `--font-size-2xl` | `20px` | Large prices |
| `--font-size-3xl` | `24px` | Price displays |
| `--font-size-4xl` | `28px` | Section headers large |
| `--font-size-5xl` | `32px` | Hero headings |
| `--font-size-6xl` | `40px` | Hero price display |

#### Spacing, Radii, Shadows, Layout (16 total — all existing, no changes)

Already tokenized: `--space-xxs` through `--space-xxl` (8), `--border-radius` (4 variants), `--box-shadow-small`, `--box-shadow-medium`, `--transition`, `--max-width`.

Components with hardcoded spacing will be updated to use the existing `--space-*` tokens where values match the scale (4px, 12px, 16px, 24px, 32px, 48px, 64px, 96px). Layout-specific values (2px border offsets, 5px nudges) stay hardcoded.

### What stays hardcoded

- **Media query breakpoints** (912px, 768px, 480px) — structural, not brand
- **Z-index values** (90, 999, 1000) — stacking context, not brand
- **Aspect ratios** (3/2, 16/10, 16/9) — content framing
- **Layout-specific px values** (2px borders, icon sizes) — micro-layout, not tokens
- **`rgba(0, 0, 0, 0.02)`** in ErgoAccordion — too subtle to theme, structural shadow

## `initTheme()` API

### ThemeConfig interface

```typescript
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
```

### Implementation

`initTheme()` maps each camelCase key to its `--css-variable` counterpart and injects a `<style>` tag with `:root` overrides. Only provided keys are emitted. Calling `initTheme({})` or `initTheme()` resets to defaults (removes the override style tag).

```typescript
const TOKEN_MAP: Record<keyof ThemeConfig, string> = {
  primary: '--color-primary',
  secondary: '--color-secondary',
  // ... all mappings
};

export function initTheme(config: ThemeConfig = {}): void {
  const entries = Object.entries(config)
    .filter(([_, v]) => v !== undefined)
    .map(([k, v]) => `${TOKEN_MAP[k as keyof ThemeConfig]}:${v}`);

  const id = 'demo-ui-lib-theme';
  let el = document.getElementById(id) as HTMLStyleElement | null;

  if (entries.length === 0) {
    el?.remove();
    return;
  }

  const css = `:root{${entries.join(';')}}`;
  if (!el) {
    el = document.createElement('style');
    el.id = id;
    document.head.appendChild(el);
  }
  el.textContent = css;
}
```

### Presets

Three preset theme objects exported from `src/theme/presets.ts`:

- **`ergoTheme`** — empty object (all defaults are ERGO). Explicit for readability.
- **`modernBlueTheme`** — `#1a56db` primary, `#2563eb` secondary, Inter font family, blue-shifted section backgrounds.
- **`warmNeutralTheme`** — `#78716c` primary, `#a8a29e` secondary, warm earth tones, softer backgrounds.

Exported from the library's main index:
```typescript
export { ergoTheme, modernBlueTheme, warmNeutralTheme } from './theme/presets';
```

## Component CSS Refactoring Rules

1. **Hex colors → `var(--token)`**: Every hardcoded color replaced with the corresponding variable. No fallback in `var()` since `:root` always defines the default.

2. **Font sizes → `var(--font-size-*)`**: Map to nearest scale step. Each hardcoded value has exactly one scale match.

3. **Spacing → `var(--space-*)`**: Replace hardcoded px with `--space-*` where the value matches (4→xxs, 12→xs, 16→s, 24→base, 32→m, 48→l, 64→xl, 96→xxl). Non-matching values (2px, 5px, 6px, 8px, 10px, 20px) stay hardcoded.

4. **Responsive overrides**: Font sizes inside `@media` blocks also use the token variables.

5. **No structural changes**: No changes to HTML, component props, or behavior. Pure CSS refactor.

## Files Changed

### Modified
- `src/theme/theme.css` — Add 7 new color variables, 11 font-size variables to `:root`
- `src/theme/index.ts` — Expand `ThemeConfig` interface, rewrite `initTheme()` with full token mapping
- `src/index.ts` — Add preset exports
- 19 ergo CSS files — Replace hardcoded values with CSS variable references

### New
- `src/theme/presets.ts` — Three preset theme objects (ergo, modernBlue, warmNeutral)

## Testing Strategy

- **Visual regression**: Run the existing demo (`npm run demo:ergo`) before and after. Pages must look identical with default theme.
- **Theme switching**: Call `initTheme(modernBlueTheme)` in browser console. All ergo components should update colors, fonts, and spacing.
- **Reset**: Call `initTheme()` to confirm reset to ERGO defaults.
- **Partial override**: Call `initTheme({ primary: '#1a56db' })` — only primary color changes, everything else stays default.
- **Build**: `npm run build` succeeds, types export correctly.

## Demo Flow (consuming app)

In the consuming app (e.g., `tlv-ergo-v4`):

1. Theme config lives in `src/config/theme.ts`:
   ```typescript
   import { initTheme } from 'demo-ui-lib';
   initTheme(); // ERGO defaults
   ```

2. During demo, Claude edits this file:
   ```typescript
   import { initTheme, modernBlueTheme } from 'demo-ui-lib';
   initTheme(modernBlueTheme);
   ```

3. Dev server hot-reloads, pages update live.

4. For custom tweaks:
   ```typescript
   import { initTheme } from 'demo-ui-lib';
   initTheme({ primary: '#0d9488', fontFamily: '"Inter", sans-serif' });
   ```
