import React from "react";

export default function Stepper({ steps, currentIndex, onSelect }) {
  return (
    <nav className="filmstrip" aria-label="Progress">
      <div className="filmstrip-track">
        {steps.map((step, i) => {
          const state = i < currentIndex ? "done" : i === currentIndex ? "active" : "upcoming";
          return (
            <button
              key={step.key}
              type="button"
              className={`filmstrip-frame is-${state}`}
              onClick={() => onSelect(i)}
              disabled={i > currentIndex}
              aria-current={i === currentIndex ? "step" : undefined}
            >
              <span className="filmstrip-sprockets" aria-hidden="true">
                <i />
                <i />
                <i />
              </span>
              <span className="filmstrip-index">{String(i + 1).padStart(2, "0")}</span>
              <span className="filmstrip-label">{step.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}