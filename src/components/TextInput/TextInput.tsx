import React, { useId } from "react";
import "./TextInput.css";

export interface TextInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  hint?: string;
  error?: string;
}

export const TextInput: React.FC<TextInputProps> = ({
  label,
  hint,
  error,
  id,
  className,
  ...props
}) => {
  const generatedId = useId();
  const inputId = id ?? generatedId;

  return (
    <div className="text-input">
      {label && (
        <label className="text-input__label" htmlFor={inputId}>
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={["text-input__field", className].filter(Boolean).join(" ")}
        data-error={error ? "true" : "false"}
        {...props}
      />
      {error && <span className="text-input__error">{error}</span>}
      {!error && hint && <span className="text-input__hint">{hint}</span>}
    </div>
  );
};
