import React from "react";
import "./Link.css";

export interface LinkProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  variant?: "default" | "muted";
}

export const Link: React.FC<LinkProps> = ({
  variant = "default",
  children,
  className,
  ...props
}) => {
  return (
    <a
      className={["link", className].filter(Boolean).join(" ")}
      data-variant={variant}
      {...props}
    >
      {children}
    </a>
  );
};
