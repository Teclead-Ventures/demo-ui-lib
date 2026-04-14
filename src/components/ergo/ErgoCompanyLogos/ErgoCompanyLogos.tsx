import React from "react";
import "./ErgoCompanyLogos.css";

export interface ErgoCompanyLogosProps {
  logos: { src: string; alt: string }[];
  className?: string;
}

export const ErgoCompanyLogos: React.FC<ErgoCompanyLogosProps> = ({
  logos,
  className,
}) => {
  return (
    <div
      className={["ergo-logos", className].filter(Boolean).join(" ")}
    >
      {logos.map((logo, i) => (
        <img
          key={i}
          className="ergo-logos__item"
          src={logo.src}
          alt={logo.alt}
          loading="lazy"
        />
      ))}
    </div>
  );
};
