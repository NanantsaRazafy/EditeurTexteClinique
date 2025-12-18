import React from "react";

export default function LineNumbers({ lines, scrollTop }) {
  return (
    <div
      className="line-numbers"
      style={{ transform: `translateY(-${scrollTop}px)` }}
    >
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="line-number">
          {i + 1}
        </div>
      ))}
    </div>
  );
}
