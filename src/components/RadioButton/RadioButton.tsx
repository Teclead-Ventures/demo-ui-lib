import React, { useId } from "react";
import "./RadioButton.css";

export interface RadioButtonProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "type"> {
  label: string;
}

export const RadioButton: React.FC<RadioButtonProps> = ({
  label,
  id,
  className,
  ...props
}) => {
  const generatedId = useId();
  const inputId = id ?? generatedId;

  return (
    <label className={["radio", className].filter(Boolean).join(" ")} htmlFor={inputId}>
      <input id={inputId} type="radio" className="radio__input" {...props} />
      <span className="radio__control" aria-hidden="true">
        <span className="radio__dot" />
      </span>
      <span className="radio__label">{label}</span>
    </label>
  );
};
