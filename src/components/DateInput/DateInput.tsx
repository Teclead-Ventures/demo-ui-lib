import React, { useId } from "react";
import "./DateInput.css";

export interface DateValue {
  day: string;
  month: string;
  year: string;
}

export interface DateInputProps {
  label?: string;
  hint?: string;
  error?: string;
  value?: DateValue;
  onChange?: (value: DateValue) => void;
  disabled?: boolean;
  id?: string;
  className?: string;
}

export const DateInput: React.FC<DateInputProps> = ({
  label,
  hint,
  error,
  value = { day: "", month: "", year: "" },
  onChange,
  disabled,
  id,
  className,
}) => {
  const generatedId = useId();
  const baseId = id ?? generatedId;

  const handleChange =
    (field: keyof DateValue) => (e: React.ChangeEvent<HTMLInputElement>) => {
      onChange?.({ ...value, [field]: e.target.value });
    };

  return (
    <div className={["date-input", className].filter(Boolean).join(" ")}>
      {label && (
        <label className="date-input__label" htmlFor={`${baseId}-day`}>
          {label}
        </label>
      )}
      <div className="date-input__fields">
        <div className="date-input__segment">
          <input
            id={`${baseId}-day`}
            type="number"
            className="date-input__field"
            min={1}
            max={31}
            placeholder="TT"
            value={value.day}
            onChange={handleChange("day")}
            disabled={disabled}
            aria-label="Tag"
          />
        </div>
        <div className="date-input__segment">
          <input
            id={`${baseId}-month`}
            type="number"
            className="date-input__field"
            min={1}
            max={12}
            placeholder="MM"
            value={value.month}
            onChange={handleChange("month")}
            disabled={disabled}
            aria-label="Monat"
          />
        </div>
        <div className="date-input__segment">
          <input
            id={`${baseId}-year`}
            type="number"
            className="date-input__field"
            style={{ width: 80 }}
            min={1900}
            max={2100}
            placeholder="JJJJ"
            value={value.year}
            onChange={handleChange("year")}
            disabled={disabled}
            aria-label="Jahr"
          />
        </div>
      </div>
      {error && <span className="date-input__error">{error}</span>}
      {!error && hint && <span className="date-input__hint">{hint}</span>}
    </div>
  );
};
