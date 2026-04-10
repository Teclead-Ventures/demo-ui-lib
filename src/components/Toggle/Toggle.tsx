import React, { useId } from "react";
import "./Toggle.css";

export interface ToggleProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "type"> {
  label: string;
}

export const Toggle: React.FC<ToggleProps> = ({ label, id, className, ...props }) => {
  const generatedId = useId();
  const inputId = id ?? generatedId;

  return (
    <label className={["toggle", className].filter(Boolean).join(" ")} htmlFor={inputId}>
      <input id={inputId} type="checkbox" className="toggle__input" {...props} />
      <span className="toggle__track" aria-hidden="true">
        <span className="toggle__thumb" />
      </span>
      <span className="toggle__label">{label}</span>
    </label>
  );
};
