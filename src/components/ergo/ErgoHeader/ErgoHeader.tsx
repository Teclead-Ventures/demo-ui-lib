import React, { useState } from "react";
import { ErgoMegaMenu, ErgoMegaMenuCategory } from "../ErgoMegaMenu";
import "./ErgoHeader.css";

export interface ErgoHeaderProps {
  logoSrc?: string;
  tagline?: string;
  categories?: ErgoMegaMenuCategory[];
  currentPage?: string;
  phoneNumber?: string;
  phoneHours?: string;
  className?: string;
}

export const ErgoHeader: React.FC<ErgoHeaderProps> = ({
  logoSrc = "https://www.ergo.de/content/dam/ergo/grafiken/logos/ERGO-Logo-ohne-Claim.svg",
  tagline = "Einfach, weil\u2019s wichtig ist.",
  categories = [],
  currentPage: _currentPage,
  phoneNumber = "0800 / 3746 095",
  phoneHours = "7-24 Uhr (geb\u00FChrenfrei)",
  className,
}) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header
      className={["ergo-header", className].filter(Boolean).join(" ")}
    >
      <div className="ergo-header__container">
        <a href="/" className="ergo-header__logo">
          <img src={logoSrc} alt="ERGO" height="32" />
          <span className="ergo-header__tagline">{tagline}</span>
        </a>

        <nav className="ergo-header__nav" aria-label="Hauptmen\u00FC">
          <button
            type="button"
            className={[
              "ergo-header__nav-btn",
              menuOpen ? "ergo-header__nav-btn--active" : "",
            ]
              .filter(Boolean)
              .join(" ")}
            onClick={() => setMenuOpen(!menuOpen)}
          >
            Versicherungen & Finanzen
          </button>
          <a href="/service" className="ergo-header__nav-link">
            Service
          </a>
          <a href="/kontakt" className="ergo-header__nav-link">
            Kontakt
          </a>
        </nav>

        <div className="ergo-header__utils">
          <button type="button" className="ergo-header__util-btn" aria-label="Suche">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
              <path d="M16 16l4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
            <span>Suche</span>
          </button>
          <a href="/berater" className="ergo-header__util-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" stroke="currentColor" strokeWidth="2" />
              <circle cx="12" cy="9" r="2.5" stroke="currentColor" strokeWidth="2" />
            </svg>
            <span>Berater</span>
          </a>
          <a href="https://kunde-s.ergo.de" className="ergo-header__util-btn" target="_blank" rel="noopener noreferrer">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2" />
            </svg>
            <span>Log-in</span>
          </a>
          <a href={`tel:${phoneNumber.replace(/\s|\//g, "")}`} className="ergo-header__phone">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.362 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.338 1.85.573 2.81.7A2 2 0 0122 16.92z" stroke="currentColor" strokeWidth="2" />
            </svg>
            <div className="ergo-header__phone-info">
              <span className="ergo-header__phone-number">{phoneNumber}</span>
              <span className="ergo-header__phone-hours">{phoneHours}</span>
            </div>
          </a>
        </div>

        <button
          type="button"
          className="ergo-header__hamburger"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Men\u00FC"
        >
          <span />
          <span />
          <span />
        </button>
      </div>

      {menuOpen && categories.length > 0 && (
        <ErgoMegaMenu
          categories={categories}
          onClose={() => setMenuOpen(false)}
        />
      )}
    </header>
  );
};
