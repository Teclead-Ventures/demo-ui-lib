import React from "react";
import "./ErgoCtaButton.css";

export interface ErgoCtaButtonProps {
  href: string;
  label: string;
  variant?: "pill" | "arrow" | "filled";
  className?: string;
  onClick?: (e: React.MouseEvent) => void;
}

export const ErgoCtaButton: React.FC<ErgoCtaButtonProps> = ({
  href,
  label,
  variant = "pill",
  className,
  onClick,
}) => {
  return (
    <a
      href={href}
      className={["ergo-cta", `ergo-cta--${variant}`, className]
        .filter(Boolean)
        .join(" ")}
      onClick={onClick}
    >
      <span className="ergo-cta__label">{label}</span>
      {variant === "arrow" && (
        <span className="ergo-cta__icon" aria-hidden="true">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path
              d="M6 3l5 5-5 5"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </span>
      )}
    </a>
  );
};
