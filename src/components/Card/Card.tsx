import React from "react";
import "./Card.css";

export interface CardProps {
  title?: string;
  children: React.ReactNode;
  cta?: string;
  onCta?: () => void;
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  title,
  children,
  cta,
  onCta,
  className,
}) => {
  return (
    <div className={["card", className].filter(Boolean).join(" ")}>
      <div className="card__body">
        {title && <div className="card__title">{title}</div>}
        <div className="card__content">{children}</div>
      </div>
      {cta && (
        <div className="card__footer">
          <button className="card__cta" onClick={onCta} type="button">
            {cta} <span aria-hidden="true">→</span>
          </button>
        </div>
      )}
    </div>
  );
};
