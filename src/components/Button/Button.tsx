import React from "react";
import "./Button.css";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  fullWidth?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = "primary",
  size = "md",
  fullWidth = false,
  children,
  className,
  ...props
}) => {
  return (
    <button
      className={["button", className].filter(Boolean).join(" ")}
      data-variant={variant}
      data-size={size}
      data-full-width={fullWidth ? "true" : "false"}
      {...props}
    >
      {children}
    </button>
  );
};
