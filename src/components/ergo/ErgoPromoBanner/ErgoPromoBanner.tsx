import React from "react";
import "./ErgoPromoBanner.css";

export interface ErgoPromoBannerProps {
  text: string;
  href: string;
  className?: string;
}

export const ErgoPromoBanner: React.FC<ErgoPromoBannerProps> = ({
  text,
  href,
  className,
}) => {
  return (
    <div
      className={["ergo-promo-banner", className].filter(Boolean).join(" ")}
    >
      <a href={href} className="ergo-promo-banner__link">
        <span>{text}</span>
        <svg
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M6 3l5 5-5 5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </a>
    </div>
  );
};
