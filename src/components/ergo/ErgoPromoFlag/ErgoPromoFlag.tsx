import React from "react";
import "./ErgoPromoFlag.css";

export interface ErgoPromoFlagProps {
  text: string;
  className?: string;
}

export const ErgoPromoFlag: React.FC<ErgoPromoFlagProps> = ({
  text,
  className,
}) => {
  return (
    <div className={["ergo-flag", className].filter(Boolean).join(" ")}>
      {text}
    </div>
  );
};
