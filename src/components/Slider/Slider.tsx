import React, { useId } from "react";
import "./Slider.css";

export interface SliderProps {
  min: number;
  max: number;
  step?: number;
  value: number;
  onChange: (value: number) => void;
  label?: string;
  unit?: string;
  formatLabel?: (value: number) => string;
  disabled?: boolean;
  id?: string;
  className?: string;
}

export const Slider: React.FC<SliderProps> = ({
  min,
  max,
  step = 1,
  value,
  onChange,
  label,
  unit,
  formatLabel,
  disabled,
  id,
  className,
}) => {
  const generatedId = useId();
  const sliderId = id ?? generatedId;

  const percent = ((value - min) / (max - min)) * 100;

  const format = formatLabel ?? ((v: number) => v.toLocaleString("de-DE"));

  const handleSlider = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(Number(e.target.value));
  };

  const handleValueInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const raw = Number(e.target.value);
    if (!isNaN(raw)) {
      onChange(Math.min(max, Math.max(min, raw)));
    }
  };

  return (
    <div className={["slider", className].filter(Boolean).join(" ")}>
      {label && (
        <label className="slider__label" htmlFor={sliderId}>
          {label}
        </label>
      )}

      <div className="slider__controls">
        <div className="slider__track-wrapper">
          <div className="slider__track-fill" />
          <div className="slider__track-progress" style={{ width: `${percent}%` }} />
          <input
            id={sliderId}
            type="range"
            className="slider__input"
            min={min}
            max={max}
            step={step}
            value={value}
            onChange={handleSlider}
            disabled={disabled}
          />
        </div>

        <input
          type="number"
          className="slider__value-input"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={handleValueInput}
          disabled={disabled}
          aria-label={label ? `${label} Wert` : "Wert"}
        />

        {unit && <span className="slider__unit">{unit}</span>}
      </div>

      <div className="slider__range-labels">
        <span>{format(min)}</span>
        <span>{format(max)}</span>
      </div>
    </div>
  );
};
