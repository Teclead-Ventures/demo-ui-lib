import React from "react";
import "./Stepper.css";

export interface StepperStep {
  label: string;
}

export interface StepperProps {
  steps: StepperStep[];
  currentStep: number; // 1-based
  className?: string;
}

export const Stepper: React.FC<StepperProps> = ({ steps, currentStep, className }) => {
  return (
    <nav
      className={["stepper", className].filter(Boolean).join(" ")}
      aria-label="Fortschritt"
    >
      {steps.map((step, index) => {
        const number = index + 1;
        const status =
          number < currentStep ? "done" : number === currentStep ? "active" : "inactive";

        return (
          <React.Fragment key={number}>
            {index > 0 && (
              <div
                className="stepper__connector"
                data-done={number <= currentStep ? "true" : "false"}
              />
            )}
            <div
              className="stepper__step"
              data-status={status}
              aria-current={status === "active" ? "step" : undefined}
            >
              <div className="stepper__circle">{number}</div>
              <span className="stepper__label">{step.label}</span>
            </div>
          </React.Fragment>
        );
      })}
    </nav>
  );
};
