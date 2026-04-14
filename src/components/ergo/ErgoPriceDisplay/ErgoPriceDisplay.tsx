import React from "react";
import "./ErgoPriceDisplay.css";

export interface ErgoPriceDisplayProps {
  prefix?: string;
  value: string;
  currency?: string;
  suffix?: string;
  size?: "auto" | "medium" | "small";
  className?: string;
}

export const ErgoPriceDisplay: React.FC<ErgoPriceDisplayProps> = ({
  prefix,
  value,
  currency = "\u20AC",
  suffix,
  size = "auto",
  className,
}) => {
  return (
    <div
      className={["ergo-price", `ergo-price--${size}`, className]
        .filter(Boolean)
        .join(" ")}
    >
      {prefix && <span className="ergo-price__prefix">{prefix}</span>}
      <span className="ergo-price__value">{value}</span>
      <span className="ergo-price__currency">{currency}</span>
      {suffix && <span className="ergo-price__suffix">{suffix}</span>}
    </div>
  );
};
