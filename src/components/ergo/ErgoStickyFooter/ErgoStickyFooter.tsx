import React, { useEffect, useRef, useState } from "react";
import { ErgoCtaButton } from "../ErgoCtaButton";
import "./ErgoStickyFooter.css";

export interface ErgoStickyFooterProps {
  productName: string;
  tariffName?: string;
  ctaLabel: string;
  ctaHref: string;
  /** CSS selector for element to observe — footer shows when this scrolls out of view */
  observeSelector?: string;
  className?: string;
}

export const ErgoStickyFooter: React.FC<ErgoStickyFooterProps> = ({
  productName,
  tariffName,
  ctaLabel,
  ctaHref,
  observeSelector = ".ergo-hero",
  className,
}) => {
  const [visible, setVisible] = useState(false);
  const observerRef = useRef<IntersectionObserver | null>(null);

  useEffect(() => {
    const target = document.querySelector(observeSelector);
    if (!target) return;

    observerRef.current = new IntersectionObserver(
      ([entry]) => {
        setVisible(!entry.isIntersecting);
      },
      { threshold: 0 }
    );
    observerRef.current.observe(target);

    return () => observerRef.current?.disconnect();
  }, [observeSelector]);

  return (
    <div
      className={[
        "ergo-sticky-footer",
        visible ? "ergo-sticky-footer--visible" : "",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <div className="ergo-sticky-footer__container">
        <div className="ergo-sticky-footer__left">
          <span className="ergo-sticky-footer__product">{productName}</span>
          {tariffName && (
            <span className="ergo-sticky-footer__tariff">{tariffName}</span>
          )}
        </div>
        <div className="ergo-sticky-footer__right">
          <ErgoCtaButton href={ctaHref} label={ctaLabel} variant="pill" />
        </div>
      </div>
    </div>
  );
};
