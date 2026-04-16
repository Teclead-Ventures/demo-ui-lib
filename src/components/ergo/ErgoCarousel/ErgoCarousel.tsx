import React, { useRef, useState, useEffect } from "react";
import "./ErgoCarousel.css";

export interface ErgoCarouselProps {
  children: React.ReactNode;
  columns?: { mobile?: number; tablet?: number; desktop?: number };
  gap?: number;
  showDots?: boolean;
  className?: string;
}

export const ErgoCarousel: React.FC<ErgoCarouselProps> = ({
  children,
  columns = { mobile: 1, tablet: 2, desktop: 3 },
  gap = 24,
  showDots = false,
  className,
}) => {
  const trackRef = useRef<HTMLDivElement>(null);
  const [currentPage, setCurrentPage] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);

  const childCount = React.Children.count(children);

  const getCols = () => {
    if (typeof window === "undefined") return columns.desktop ?? 3;
    if (window.innerWidth <= 480) return columns.mobile ?? 1;
    if (window.innerWidth <= 768) return columns.tablet ?? 2;
    return columns.desktop ?? 3;
  };

  const updateState = () => {
    const el = trackRef.current;
    if (!el) return;

    const pages = Math.ceil(childCount / getCols());
    setTotalPages(pages);

    // current page = which full-width scroll position we're at
    const page = el.clientWidth > 0
      ? Math.round(el.scrollLeft / el.clientWidth)
      : 0;
    setCurrentPage(Math.min(page, pages - 1));

    setCanScrollLeft(el.scrollLeft > 1);
    setCanScrollRight(el.scrollLeft < el.scrollWidth - el.clientWidth - 1);
  };

  useEffect(() => {
    updateState();
    const el = trackRef.current;
    if (!el) return;
    el.addEventListener("scroll", updateState, { passive: true });
    const ro = new ResizeObserver(updateState);
    ro.observe(el);
    return () => {
      el.removeEventListener("scroll", updateState);
      ro.disconnect();
    };
  }, []);

  const scrollToPage = (page: number) => {
    const el = trackRef.current;
    if (!el) return;
    el.scrollTo({ left: page * el.clientWidth, behavior: "smooth" });
  };

  const scroll = (dir: "left" | "right") => {
    const el = trackRef.current;
    if (!el) return;
    // scroll by exactly one full page width so we land on the next group
    el.scrollBy({ left: dir === "left" ? -el.clientWidth : el.clientWidth, behavior: "smooth" });
  };

  const style = {
    "--carousel-cols-mobile": columns.mobile,
    "--carousel-cols-tablet": columns.tablet,
    "--carousel-cols-desktop": columns.desktop,
    "--carousel-gap": `${gap}px`,
  } as React.CSSProperties;

  const showNav = totalPages > 1;

  return (
    <div
      className={["ergo-carousel", className].filter(Boolean).join(" ")}
      style={style}
    >
      <div className="ergo-carousel__track" ref={trackRef}>
        {children}
      </div>

      {showNav && (
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

          {showDots && (
            <div className="ergo-carousel__dots">
              {Array.from({ length: totalPages }).map((_, i) => (
                <button
                  key={i}
                  type="button"
                  className={[
                    "ergo-carousel__dot",
                    i === currentPage ? "ergo-carousel__dot--active" : "",
                  ].filter(Boolean).join(" ")}
                  onClick={() => scrollToPage(i)}
                  aria-label={`Seite ${i + 1}`}
                />
              ))}
            </div>
          )}

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
