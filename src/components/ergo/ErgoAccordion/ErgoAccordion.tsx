import React, { useState } from "react";
import "./ErgoAccordion.css";

export interface ErgoAccordionItem {
  title: string;
  content: React.ReactNode;
}

export interface ErgoAccordionProps {
  items: ErgoAccordionItem[];
  allowMultiple?: boolean;
  className?: string;
}

export const ErgoAccordion: React.FC<ErgoAccordionProps> = ({
  items,
  allowMultiple = false,
  className,
}) => {
  const [openIndices, setOpenIndices] = useState<Set<number>>(new Set());

  const toggle = (index: number) => {
    setOpenIndices((prev) => {
      const next = new Set(allowMultiple ? prev : []);
      if (prev.has(index)) {
        next.delete(index);
      } else {
        next.add(index);
      }
      return next;
    });
  };

  return (
    <div
      className={["ergo-accordion", className].filter(Boolean).join(" ")}
    >
      {items.map((item, index) => {
        const isOpen = openIndices.has(index);
        return (
          <div
            key={index}
            className={[
              "ergo-accordion__item",
              isOpen ? "ergo-accordion__item--open" : "",
            ]
              .filter(Boolean)
              .join(" ")}
          >
            <button
              type="button"
              className="ergo-accordion__trigger"
              onClick={() => toggle(index)}
              aria-expanded={isOpen}
            >
              <span className="ergo-accordion__title">{item.title}</span>
              <svg
                className="ergo-accordion__chevron"
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
            <div className="ergo-accordion__panel" role="region">
              <div className="ergo-accordion__content">{item.content}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
