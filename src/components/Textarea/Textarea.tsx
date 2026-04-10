import React, { useId } from "react";
import "./Textarea.css";

export interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  hint?: string;
  error?: string;
}

export const Textarea: React.FC<TextareaProps> = ({
  label,
  hint,
  error,
  id,
  rows = 4,
  className,
  ...props
}) => {
  const generatedId = useId();
  const fieldId = id ?? generatedId;

  return (
    <div className="textarea">
      {label && (
        <label className="textarea__label" htmlFor={fieldId}>
          {label}
        </label>
      )}
      <textarea
        id={fieldId}
        rows={rows}
        className={["textarea__field", className].filter(Boolean).join(" ")}
        data-error={error ? "true" : "false"}
        {...props}
      />
      {error && <span className="textarea__error">{error}</span>}
      {!error && hint && <span className="textarea__hint">{hint}</span>}
    </div>
  );
};
