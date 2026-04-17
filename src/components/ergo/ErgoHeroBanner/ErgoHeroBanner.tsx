import React from "react";
import { ErgoCtaButton, ErgoCtaButtonProps } from "../ErgoCtaButton";
import { ErgoPriceDisplay, ErgoPriceDisplayProps } from "../ErgoPriceDisplay";
import "./ErgoHeroBanner.css";

export interface ErgoHeroBannerProps {
  image: string;
  imageAlt?: string;
  title?: string;
  headline?: string;
  description?: string;
  price?: ErgoPriceDisplayProps;
  ctas?: ErgoCtaButtonProps[];
  storerImage?: string;
  variant?: "full" | "short";
  textPosition?: "left" | "right";
  bgColor?: string;
  className?: string;
}

export const ErgoHeroBanner: React.FC<ErgoHeroBannerProps> = ({
  image,
  imageAlt = "",
  title,
  headline,
  description,
  price,
  ctas = [],
  storerImage,
  variant = "full",
  textPosition = "right",
  bgColor,
  className,
}) => {
  return (
    <div
      className={["ergo-hero", `ergo-hero--${variant}`, textPosition === "left" ? "ergo-hero--text-left" : "", className]
        .filter(Boolean)
        .join(" ")}
      style={bgColor ? { backgroundColor: bgColor } : undefined}
    >
      <div className="ergo-hero__grid">
        <div className="ergo-hero__image">
          <img src={image} alt={imageAlt} loading="eager" />
        </div>
        <div className="ergo-hero__teaser">
          {title && <div className="ergo-hero__title">{title}</div>}
          {headline && <h1 className="ergo-hero__headline">{headline}</h1>}
          {description && (
            <p className="ergo-hero__description">{description}</p>
          )}
          {price && (
            <div className="ergo-hero__price">
              <ErgoPriceDisplay {...price} size="auto" />
            </div>
          )}
          {ctas.length > 0 && (
            <div className="ergo-hero__actions">
              {ctas.map((cta, i) => (
                <ErgoCtaButton key={i} {...cta} />
              ))}
            </div>
          )}
        </div>
        {storerImage && (
          <div className="ergo-hero__storer">
            <img src={storerImage} alt="" loading="lazy" />
          </div>
        )}
      </div>
    </div>
  );
};
