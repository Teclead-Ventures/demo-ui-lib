import React from "react";
import "./ErgoDownloadLink.css";

export interface ErgoDownloadLinkProps {
  title: string;
  href: string;
  fileType?: string;
  fileSize?: string;
  className?: string;
}

export const ErgoDownloadLink: React.FC<ErgoDownloadLinkProps> = ({
  title,
  href,
  fileType,
  fileSize,
  className,
}) => {
  return (
    <a
      href={href}
      className={["ergo-download", className].filter(Boolean).join(" ")}
      target="_blank"
      rel="noopener noreferrer"
    >
      <svg
        className="ergo-download__icon"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M12 3v12m0 0l-4-4m4 4l4-4M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      <div className="ergo-download__info">
        <span className="ergo-download__title">{title}</span>
        {(fileType || fileSize) && (
          <span className="ergo-download__meta">
            {[fileType, fileSize].filter(Boolean).join(" \u00B7 ")}
          </span>
        )}
      </div>
    </a>
  );
};
