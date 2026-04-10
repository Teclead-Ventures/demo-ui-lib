import React from "react";
import "./Tooltip.css";

export interface TooltipProps {
  content: string;
  position?: "top" | "bottom" | "left" | "right";
  children: React.ReactNode;
  className?: string;
}

export const Tooltip: React.FC<TooltipProps> = ({
  content,
  position = "top",
  children,
  className,
}) => {
  return (
    <span className={["tooltip", className].filter(Boolean).join(" ")}>
      {children}
      <span className="tooltip__bubble" data-position={position} role="tooltip">
        {content}
      </span>
    </span>
  );
};
