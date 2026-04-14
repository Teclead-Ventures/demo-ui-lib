import React, { useRef, useState, useEffect } from "react";
import "./ErgoCarousel.css";

export interface ErgoCarouselProps {
  children: React.ReactNode;
  columns?: { mobile?: number; tablet?: number; desktop?: number };
  gap?: number;
  className?: string;
}

export const ErgoCarousel: React.FC<ErgoCarouselProps> = ({
  children,
  columns = { mobile: 1, tablet: 2, desktop: 3 },
  gap = 24,
  className,
}) => {
  const trackRef = useRef<HTMLDivElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);

  const updateScrollState = () => {
    const el = trackRef.current;
    if (!el) return;
    setCanScrollLeft(el.scrollLeft > 1);
    setCanScrollRight(el.scrollLeft < el.scrollWidth - el.clientWidth - 1);
  };

  useEffect(() => {
    updateScrollState();
    const el = trackRef.current;
    if (!el) return;
    el.addEventListener("scroll", updateScrollState, { passive: true });
    const ro = new ResizeObserver(updateScrollState);
    ro.observe(el);
    return () => {
      el.removeEventListener("scroll", updateScrollState);
      ro.disconnect();
    };
  }, []);

  const scroll = (dir: "left" | "right") => {
    const el = trackRef.current;
    if (!el) return;
    const amount = el.clientWidth * 0.8;
    el.scrollBy({ left: dir === "left" ? -amount : amount, behavior: "smooth" });
  };

  const style = {
    "--carousel-cols-mobile": columns.mobile,
    "--carousel-cols-tablet": columns.tablet,
    "--carousel-cols-desktop": columns.desktop,
    "--carousel-gap": `${gap}px`,
  } as React.CSSProperties;

  return (
    <div
      className={["ergo-carousel", className].filter(Boolean).join(" ")}
      style={style}
    >
      <div className="ergo-carousel__track" ref={trackRef}>
        {children}
      </div>
      {(canScrollLeft || canScrollRight) && (
        <div className="ergo-carousel__nav">
          <button
            type="button"
            className="ergo-carousel__btn"
            onClick={() => scroll("left")}
            disabled={!canScrollLeft}
            aria-label="Vorherige"
          >
            <svg width="20" height="20" viewBox="0 0 16 16" fill="none">
              <path d="M10 3L5 8l5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
          <button
            type="button"
            className="ergo-carousel__btn"
            onClick={() => scroll("right")}
            disabled={!canScrollRight}
            aria-label="Nächste"
          >
            <svg width="20" height="20" viewBox="0 0 16 16" fill="none">
              <path d="M6 3l5 5-5 5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};
