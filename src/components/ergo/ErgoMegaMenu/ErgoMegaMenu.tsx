import React, { useState } from "react";
import { ErgoCtaButton } from "../ErgoCtaButton";
import "./ErgoMegaMenu.css";

export interface ErgoMegaMenuSubItem {
  label: string;
  href: string;
}

export interface ErgoMegaMenuCategory {
  label: string;
  items: ErgoMegaMenuSubItem[];
}

export interface ErgoMegaMenuPromo {
  title: string;
  price?: string;
  ctaLabel: string;
  ctaHref: string;
}

export interface ErgoMegaMenuProps {
  categories: ErgoMegaMenuCategory[];
  promo?: ErgoMegaMenuPromo;
  onClose: () => void;
  className?: string;
}

export const ErgoMegaMenu: React.FC<ErgoMegaMenuProps> = ({
  categories,
  promo,
  onClose,
  className,
}) => {
  const [activeCategory, setActiveCategory] = useState<number | null>(null);

  return (
    <div className={["ergo-mega", className].filter(Boolean).join(" ")}>
      <div className="ergo-mega__container">
        <div className="ergo-mega__header">
          <span className="ergo-mega__title">Versicherungen & Finanzen</span>
          <button
            type="button"
            className="ergo-mega__close"
            onClick={onClose}
            aria-label="Schlie\u00DFen"
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M5 5l10 10M15 5L5 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
            <span>Schlie\u00DFen</span>
          </button>
        </div>

        <div className="ergo-mega__body">
          <ul className="ergo-mega__categories">
            {categories.map((cat, i) => (
              <li key={i}>
                <button
                  type="button"
                  className={[
                    "ergo-mega__cat-btn",
                    activeCategory === i ? "ergo-mega__cat-btn--active" : "",
                  ]
                    .filter(Boolean)
                    .join(" ")}
                  onClick={() =>
                    setActiveCategory(activeCategory === i ? null : i)
                  }
                >
                  <span>{cat.label}</span>
                  {cat.items.length > 0 && (
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                      <path d="M6 3l5 5-5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  )}
                </button>
              </li>
            ))}
          </ul>

          {activeCategory !== null && categories[activeCategory]?.items.length > 0 && (
            <ul className="ergo-mega__subitems">
              {categories[activeCategory].items.map((item, i) => (
                <li key={i}>
                  <a href={item.href} className="ergo-mega__sublink">
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          )}

          {promo && (
            <div className="ergo-mega__promo">
              <div className="ergo-mega__promo-title">{promo.title}</div>
              {promo.price && (
                <div className="ergo-mega__promo-price">{promo.price}</div>
              )}
              <ErgoCtaButton
                href={promo.ctaHref}
                label={promo.ctaLabel}
                variant="pill"
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
