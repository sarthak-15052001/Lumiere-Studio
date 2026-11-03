import React from "react";

const BACKGROUNDS = [
  "Solid White",
  "Solid Black",
  "Transparent (Isolated)",
  "Workspace",
  "Office",
  "Professional Studio",
  "City",
  "Urban",
  "Historic",
  "Ancient",
  "HomeVibe",
  "Custom Idea",
];

const STYLE_PRESETS = ["Modern", "Minimalist", "Vintage", "Monochrome", "Aesthetic", "Close-up"];
const APPAREL_STYLES = ["Professional", "Casual"];

export default function CustomizeStep({ form, updateForm }) {
  return (
    <>
      <div className="stage-head">
        <span className="stage-eyebrow">03 · Customize</span>
        <h1 className="stage-title">Set the look and feel</h1>
        <p className="stage-sub">
          Choose the background and the overall style.
        </p>
      </div>

      <div className="field-group">
        <span className="field-label">Background</span>
        <div className="chip-row">
          {BACKGROUNDS.map((b) => (
            <button
              key={b}
              type="button"
              className={`chip ${form.background === b ? "is-selected" : ""}`}
              onClick={() => updateForm({ background: b })}
            >
              {b}
            </button>
          ))}
        </div>
        {form.background === "Custom Idea" && (
          <input
            className="text-input"
            placeholder="Describe the background you have in mind..."
            value={form.customBackground}
            onChange={(e) => updateForm({ customBackground: e.target.value })}
            maxLength={150}
          />
        )}
      </div>

      <div className="field-group">
        <span className="field-label">Style Preset</span>
        <div className="chip-row">
          {STYLE_PRESETS.map((s) => (
            <button
              key={s}
              type="button"
              className={`chip ${form.stylePreset === s ? "is-selected" : ""}`}
              onClick={() => updateForm({ stylePreset: s })}
            >
              {s}
            </button>
          ))}
        </div>
      </div>

      <div className="field-group">
        <span className="field-label">Apparel Style</span>
        <div className="chip-row">
          {APPAREL_STYLES.map((s) => (
            <button
              key={s}
              type="button"
              className={`chip ${form.apparelStyle === s ? "is-selected" : ""}`}
              onClick={() => updateForm({ apparelStyle: s })}
            >
              {s}
            </button>
          ))}
        </div>
      </div>
    </>
  );
}