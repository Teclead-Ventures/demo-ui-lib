import React, { useId } from "react";
import "./SegmentedControl.css";

export interface SegmentedControlOption {
  value: string;
  label: string;
}

export interface SegmentedControlProps {
  name?: string;
  options: SegmentedControlOption[];
  value: string;
  onChange: (value: string) => void;
}

export const SegmentedControl: React.FC<SegmentedControlProps> = ({
  name,
  options,
  value,
  onChange,
}) => {
  const generatedName = useId();
  const inputName = name ?? generatedName;

  return (
    <div className="segmented-control" role="radiogroup">
      {options.map((opt) => (
        <label
          key={opt.value}
          className="segmented-control__option"
          data-checked={value === opt.value ? "true" : "false"}
        >
          <input
            type="radio"
            className="segmented-control__input"
            name={inputName}
            value={opt.value}
            checked={value === opt.value}
            onChange={() => onChange(opt.value)}
          />
          <span className="segmented-control__label">{opt.label}</span>
          <span className="segmented-control__indicator" aria-hidden="true">
            <span className="segmented-control__dot" />
          </span>
        </label>
      ))}
    </div>
  );
};
