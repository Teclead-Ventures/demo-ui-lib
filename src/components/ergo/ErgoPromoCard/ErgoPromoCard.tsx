import React from "react";
import { ErgoCtaButton, ErgoCtaButtonProps } from "../ErgoCtaButton";
import { ErgoPriceDisplay, ErgoPriceDisplayProps } from "../ErgoPriceDisplay";
import { ErgoPromoFlag } from "../ErgoPromoFlag";
import "./ErgoPromoCard.css";

export interface ErgoPromoCardProps {
  image: string;
  imageAlt?: string;
  headline: string;
  description?: string;
  price?: ErgoPriceDisplayProps;
  badge?: string;
  flag?: string;
  ctas?: ErgoCtaButtonProps[];
  layout?: "vertical" | "horizontal";
  bgColor?: string;
  className?: string;
}

export const ErgoPromoCard: React.FC<ErgoPromoCardProps> = ({
  image,
  imageAlt = "",
  headline,
  description,
  price,
  badge,
  flag,
  ctas = [],
  layout = "vertical",
  bgColor,
  className,
}) => {
  return (
    <div
      className={[
        "ergo-promo",
        `ergo-promo--${layout}`,
        className,
      ]
        .filter(Boolean)
        .join(" ")}
      style={bgColor ? { backgroundColor: bgColor, borderColor: "transparent" } : undefined}
    >
      <div className="ergo-promo__image-container">
        <img
          className="ergo-promo__image"
          src={image}
          alt={imageAlt}
          loading="lazy"
        />
        {badge && (
          <img
            className="ergo-promo__badge"
            src={badge}
            alt=""
            loading="lazy"
          />
        )}
        {flag && (
          <div className="ergo-promo__flag-wrapper">
            <ErgoPromoFlag text={flag} />
          </div>
        )}
      </div>

      <div className="ergo-promo__content">
        <h3 className="ergo-promo__headline">{headline}</h3>
        {description && (
          <p className="ergo-promo__description">{description}</p>
        )}
        {price && (
          <div className="ergo-promo__price">
            <ErgoPriceDisplay
              {...price}
              size={layout === "horizontal" ? "medium" : "medium"}
            />
          </div>
        )}
        {ctas.length > 0 && (
          <div className="ergo-promo__actions">
            {ctas.map((cta, i) => (
              <ErgoCtaButton key={i} {...cta} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
