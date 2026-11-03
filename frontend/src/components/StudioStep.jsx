import React from "react";
import { CATEGORIES, getSubcategories } from "../config/categories.js";

const STUDIO_TYPES = [
  {
    value: "Photo Studio",
    title: "Photo Studio",
    desc: "Clean catalog shots on a plain backdrop. Best for e-commerce listings.",
  },
  {
    value: "Marketing Studio",
    title: "Marketing Studio",
    desc: "Dynamic, campaign-style imagery with cinematic lighting and mood.",
  },
  {
    value: "Custom Model Studio",
    title: "Custom Model Studio",
    desc: "Upload your own model reference photo instead of an AI-generated one.",
  },
];

export default function StudioStep({ form, updateForm }) {
  const subcategories = getSubcategories(form.category);
  const isDualMode = form.studioType === "Custom Model Studio";

  const handleCategoryChange = (categoryValue) => {
    const firstSub = getSubcategories(categoryValue)[0];
    updateForm({
      category: categoryValue,
      targetAudience: firstSub.value,
      // Custom Model Studio supplies its own model image, so region doesn't
      // apply there — leave whatever it was in that case.
      region: isDualMode ? form.region : firstSub.defaultRegion,
    });
  };

  const handleSubcategoryChange = (sub) => {
    updateForm({
      targetAudience: sub.value,
      region: isDualMode ? form.region : sub.defaultRegion,
    });
  };

  return (
    <>
      <div className="stage-head">
        <span className="stage-eyebrow">01 · Choose Studio</span>
        <h1 className="stage-title">What are we shooting today?</h1>
        <p className="stage-sub">
          Pick a studio type and the product category. This decides how the AI frames and lights
          your shot.
        </p>
      </div>

      <div className="field-group">
        <span className="field-label">Studio Type</span>
        <div className="choice-grid">
          {STUDIO_TYPES.map((s) => (
            <button
              key={s.value}
              type="button"
              className={`choice-card ${form.studioType === s.value ? "is-selected" : ""}`}
              onClick={() => updateForm({ studioType: s.value })}
            >
              <span className="choice-card-title">{s.title}</span>
              <span className="choice-card-desc">{s.desc}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="field-group">
        <span className="field-label">Category</span>
        <div className="chip-row">
          {CATEGORIES.map((c) => (
            <button
              key={c.value}
              type="button"
              className={`chip ${form.category === c.value ? "is-selected" : ""}`}
              onClick={() => handleCategoryChange(c.value)}
            >
              {c.label}
            </button>
          ))}
        </div>
      </div>

      <div className="field-group">
        <span className="field-label">Subcategory</span>
        <p className="hint">
          This also sets who or what the AI shoots for — used directly in the generation prompt.
        </p>
        <div className="chip-row">
          {subcategories.map((sub) => (
            <button
              key={sub.value}
              type="button"
              className={`chip ${form.targetAudience === sub.value ? "is-selected" : ""}`}
              onClick={() => handleSubcategoryChange(sub)}
            >
              {sub.label}
            </button>
          ))}
        </div>
      </div>
    </>
  );
}