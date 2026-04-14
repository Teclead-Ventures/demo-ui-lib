import React from "react";
import "./ErgoReviewSection.css";

export interface ErgoReviewSectionProps {
  quote: string;
  rating: number;
  reviewCount: string;
  companyName: string;
  className?: string;
}

export const ErgoReviewSection: React.FC<ErgoReviewSectionProps> = ({
  quote,
  rating,
  reviewCount,
  companyName,
  className,
}) => {
  const fullStars = Math.floor(rating);
  const hasHalf = rating % 1 >= 0.3;

  return (
    <div
      className={["ergo-review", className].filter(Boolean).join(" ")}
    >
      <blockquote className="ergo-review__quote">{quote}</blockquote>
      <div className="ergo-review__rating">
        <div className="ergo-review__stars" aria-label={`${rating} von 5 Sternen`}>
          {Array.from({ length: 5 }, (_, i) => (
            <svg key={i} width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path
                d="M10 1.5l2.47 5.01 5.53.8-4 3.9.94 5.49L10 14.27 5.06 16.7 6 11.21l-4-3.9 5.53-.8L10 1.5z"
                fill={i < fullStars || (i === fullStars && hasHalf) ? "#f6cb00" : "#e1e1e1"}
                stroke={i < fullStars || (i === fullStars && hasHalf) ? "#f6cb00" : "#e1e1e1"}
                strokeWidth="1"
              />
            </svg>
          ))}
        </div>
        <span className="ergo-review__score">{rating}/5</span>
      </div>
      <div className="ergo-review__meta">
        Ermittelt aus <strong>{reviewCount}</strong> Bewertungen
      </div>
      <div className="ergo-review__company">{companyName}</div>
    </div>
  );
};
