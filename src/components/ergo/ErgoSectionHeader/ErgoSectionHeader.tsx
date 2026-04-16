import React from "react";
import "./ErgoSectionHeader.css";

export interface ErgoSectionHeaderProps {
  label?: string;
  heading: string;
  subtitle?: string;
  headingPrimary?: boolean;
  className?: string;
}

export const ErgoSectionHeader: React.FC<ErgoSectionHeaderProps> = ({
  label,
  heading,
  subtitle,
  headingPrimary = false,
  className,
}) => {
  return (
    <div
      className={["ergo-section-header", className].filter(Boolean).join(" ")}
    >
      {label && <div className="ergo-section-header__label">{label}</div>}
      <h2 className={["ergo-section-header__heading", headingPrimary ? "ergo-section-header__heading--primary" : ""].filter(Boolean).join(" ")}>{heading}</h2>
      {subtitle && (
        <p className="ergo-section-header__subtitle">{subtitle}</p>
      )}
    </div>
  );
};
