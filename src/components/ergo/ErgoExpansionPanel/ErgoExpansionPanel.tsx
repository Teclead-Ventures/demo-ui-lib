import React, { useState } from "react";
import "./ErgoExpansionPanel.css";

export interface ErgoExpansionPanelProps {
  buttonText: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
  className?: string;
}

export const ErgoExpansionPanel: React.FC<ErgoExpansionPanelProps> = ({
  buttonText,
  children,
  defaultOpen = false,
  className,
}) => {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div
      className={[
        "ergo-expansion",
        open ? "ergo-expansion--open" : "",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <button
        type="button"
        className="ergo-expansion__button"
        onClick={() => setOpen(!open)}
        aria-expanded={open}
      >
        <span>{buttonText}</span>
        <svg
          className="ergo-expansion__icon"
          width="16"
          height="16"
          viewBox="0 0 16 16"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M4 6l4 4 4-4"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>
      <div className="ergo-expansion__panel">
        <div className="ergo-expansion__content">{children}</div>
      </div>
    </div>
  );
};
