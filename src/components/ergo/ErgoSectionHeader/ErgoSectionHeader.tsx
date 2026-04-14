import React from "react";
import "./ErgoSectionHeader.css";

export interface ErgoSectionHeaderProps {
  label?: string;
  heading: string;
  subtitle?: string;
  className?: string;
}

export const ErgoSectionHeader: React.FC<ErgoSectionHeaderProps> = ({
  label,
  heading,
  subtitle,
  className,
}) => {
  return (
    <div
      className={["ergo-section-header", className].filter(Boolean).join(" ")}
    >
      {label && <div className="ergo-section-header__label">{label}</div>}
      <h2 className="ergo-section-header__heading">{heading}</h2>
      {subtitle && (
        <p className="ergo-section-header__subtitle">{subtitle}</p>
      )}
    </div>
  );
};
