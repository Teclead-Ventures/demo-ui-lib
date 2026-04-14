import React from "react";
import { ErgoCtaButton } from "../ErgoCtaButton";
import "./ErgoArticleTeaser.css";

export interface ErgoArticleTeaserProps {
  headline: string;
  subhead?: string;
  text?: string;
  ctaLabel?: string;
  ctaHref?: string;
  className?: string;
}

export const ErgoArticleTeaser: React.FC<ErgoArticleTeaserProps> = ({
  headline,
  subhead,
  text,
  ctaLabel,
  ctaHref,
  className,
}) => {
  return (
    <div
      className={["ergo-article-teaser", className].filter(Boolean).join(" ")}
    >
      <h3 className="ergo-article-teaser__headline">{headline}</h3>
      {subhead && (
        <div className="ergo-article-teaser__subhead">{subhead}</div>
      )}
      {text && <p className="ergo-article-teaser__text">{text}</p>}
      {ctaLabel && ctaHref && (
        <div className="ergo-article-teaser__cta">
          <ErgoCtaButton href={ctaHref} label={ctaLabel} variant="arrow" />
        </div>
      )}
    </div>
  );
};
