import React, { useId } from "react";
import "./InlineRadio.css";

export interface InlineRadioOption {
  value: string;
  label: string;
}

export interface InlineRadioProps {
  name?: string;
  label?: string;
  options: InlineRadioOption[];
  value?: string;
  onChange?: (value: string) => void;
  disabled?: boolean;
}

export const InlineRadio: React.FC<InlineRadioProps> = ({
  name,
  label,
  options,
  value,
  onChange,
  disabled = false,
}) => {
  const generatedName = useId();
  const inputName = name ?? generatedName;

  return (
    <div className="inline-radio">
      {label && <span className="inline-radio__label">{label}</span>}
      <div className="inline-radio__options">
        {options.map((opt) => (
          <label
            key={opt.value}
            className="inline-radio__option"
            data-disabled={disabled ? "true" : "false"}
          >
            <input
              type="radio"
              className="inline-radio__input"
              name={inputName}
              value={opt.value}
              checked={value === opt.value}
              onChange={() => onChange?.(opt.value)}
              disabled={disabled}
            />
            <span className="inline-radio__control" aria-hidden="true">
              <span className="inline-radio__dot" />
            </span>
            <span className="inline-radio__option-label">{opt.label}</span>
          </label>
        ))}
      </div>
    </div>
  );
};
