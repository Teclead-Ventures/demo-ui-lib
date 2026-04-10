import React, { useId } from "react";
import "./RadioButton.css";

export interface RadioButtonProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "type"> {
  label: string;
  description?: string;
}

export const RadioButton: React.FC<RadioButtonProps> = ({
  label,
  description,
  id,
  className,
  ...props
}) => {
  const generatedId = useId();
  const inputId = id ?? generatedId;

  return (
    <label className={["radio", className].filter(Boolean).join(" ")} htmlFor={inputId}>
      <input id={inputId} type="radio" className="radio__input" {...props} />
      <span className="radio__text">
        <span className="radio__label">{label}</span>
        {description && <span className="radio__description">{description}</span>}
      </span>
    </label>
  );
};
