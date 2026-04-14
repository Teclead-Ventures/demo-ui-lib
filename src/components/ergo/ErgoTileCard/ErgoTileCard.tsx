import React from "react";
import "./ErgoTileCard.css";

export interface ErgoTileCardProps {
  icon?: string;
  title: string;
  text?: string;
  stat?: string;
  ctaLabel?: string;
  ctaHref?: string;
  variant?: "icon" | "stat" | "contact" | "link";
  bgColor?: string;
  className?: string;
}

export const ErgoTileCard: React.FC<ErgoTileCardProps> = ({
  icon,
  title,
  text,
  stat,
  ctaLabel,
  ctaHref,
  variant = "icon",
  bgColor,
  className,
}) => {
  return (
    <div
      className={["ergo-tile", `ergo-tile--${variant}`, className]
        .filter(Boolean)
        .join(" ")}
      style={bgColor ? { backgroundColor: bgColor } : undefined}
    >
      {icon && (
        <div className="ergo-tile__icon">
          <img src={icon} alt="" width="48" height="48" />
        </div>
      )}
      {stat && <div className="ergo-tile__stat">{stat}</div>}
      <div className="ergo-tile__title">{title}</div>
      {text && <div className="ergo-tile__text">{text}</div>}
      {ctaLabel && ctaHref && (
        <a href={ctaHref} className="ergo-tile__cta">
          <span>{ctaLabel}</span>
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
      )}
    </div>
  );
};
