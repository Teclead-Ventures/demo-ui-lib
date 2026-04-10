import React from "react";
import "./Alert.css";

export type AlertVariant = "info" | "success" | "warning" | "error";

export interface AlertProps {
  variant?: AlertVariant;
  children: React.ReactNode;
  className?: string;
}

export const Alert: React.FC<AlertProps> = ({
  variant = "info",
  children,
  className,
}) => {
  return (
    <div
      className={["alert", className].filter(Boolean).join(" ")}
      data-variant={variant}
      role="alert"
    >
      {children}
    </div>
  );
};
