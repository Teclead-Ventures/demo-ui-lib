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
  const root = document.documentElement;

  // Clear all previous overrides
  Object.values(TOKEN_MAP).forEach((v) => root.style.removeProperty(v));

  // Apply new overrides via setProperty (injection-safe)
  Object.entries(config)
    .filter(([_, v]) => v !== undefined)
    .forEach(([k, v]) =>
      root.style.setProperty(TOKEN_MAP[k as keyof ThemeConfig], v as string)
    );
}
