import "./theme.css";

export interface ThemeConfig {
  primary?: string;
  secondary?: string;
}

export function initTheme(config: ThemeConfig = {}): void {
  const { primary = "#8c003c", secondary = "#6b6b6b" } = config;
  const id = "demo-ui-lib-theme";

  const css = `:root{--color-primary:${primary};--color-secondary:${secondary};}`;

  let el = document.getElementById(id) as HTMLStyleElement | null;
  if (!el) {
    el = document.createElement("style");
    el.id = id;
    document.head.appendChild(el);
  }
  el.textContent = css;
}
