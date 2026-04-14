import React from "react";
import "./ErgoFooter.css";

export interface ErgoFooterLinkGroup {
  title: string;
  links: { label: string; href: string }[];
}

export interface ErgoFooterProps {
  linkGroups?: ErgoFooterLinkGroup[];
  legalText?: string;
  className?: string;
}

export const ErgoFooter: React.FC<ErgoFooterProps> = ({
  linkGroups = [],
  legalText = "\u00A9 2026 ERGO. Alle Rechte vorbehalten.",
  className,
}) => {
  return (
    <footer
      className={["ergo-footer", className].filter(Boolean).join(" ")}
    >
      <div className="ergo-footer__container">
        {linkGroups.length > 0 && (
          <div className="ergo-footer__links">
            {linkGroups.map((group, i) => (
              <div key={i} className="ergo-footer__group">
                <h4 className="ergo-footer__group-title">{group.title}</h4>
                <ul className="ergo-footer__group-list">
                  {group.links.map((link, j) => (
                    <li key={j}>
                      <a href={link.href} className="ergo-footer__link">
                        {link.label}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}

        <div className="ergo-footer__bottom">
          <div className="ergo-footer__legal">{legalText}</div>
          <div className="ergo-footer__social">
            <a
              href="https://www.facebook.com/ERGO"
              aria-label="Facebook"
              target="_blank"
              rel="noopener noreferrer"
              className="ergo-footer__social-link"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" />
              </svg>
            </a>
            <a
              href="https://www.instagram.com/ergo_deutschland"
              aria-label="Instagram"
              target="_blank"
              rel="noopener noreferrer"
              className="ergo-footer__social-link"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="2" y="2" width="20" height="20" rx="5" />
                <circle cx="12" cy="12" r="5" />
                <circle cx="17.5" cy="6.5" r="1.5" fill="currentColor" stroke="none" />
              </svg>
            </a>
            <a
              href="https://www.youtube.com/ergo"
              aria-label="YouTube"
              target="_blank"
              rel="noopener noreferrer"
              className="ergo-footer__social-link"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M22.54 6.42a2.78 2.78 0 00-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 00-1.94 2A29 29 0 001 11.75a29 29 0 00.46 5.33A2.78 2.78 0 003.4 19.1c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 001.94-2 29 29 0 00.46-5.25 29 29 0 00-.46-5.43z" />
                <path d="M9.75 15.02l5.75-3.27-5.75-3.27v6.54z" fill="#fff" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
