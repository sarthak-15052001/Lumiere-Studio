import React, { useEffect, useState } from "react";
import { resolveAssetUrl } from "../api/client.js";
import { getSubcategories } from "../config/categories.js";

const GEN_STEPS = ["Uploading", "Analyzing Product", "Rendering", "Finalizing"];
const STEP_ADVANCE_MS = 2200;

function GenerationTimeline({ active }) {
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    if (!active) {
      setStepIndex(0);
      return;
    }
    const interval = setInterval(() => {
      setStepIndex((i) => Math.min(i + 1, GEN_STEPS.length - 1));
    }, STEP_ADVANCE_MS);
    return () => clearInterval(interval);
  }, [active]);

  return (
    <div className="gen-progress">
      <div className="gen-progress-steps">
        {GEN_STEPS.map((label, i) => (
          <div
            key={label}
            className={`gen-progress-step ${i < stepIndex ? "is-done" : ""} ${i === stepIndex ? "is-active" : ""}`}
          >
            <div className="gen-progress-track" />
            <div className="gen-progress-node">{i < stepIndex ? "✓" : i + 1}</div>
            <span className="gen-progress-label">{label}</span>
          </div>
        ))}
      </div>
      <p className="hint" style={{ textAlign: "center" }}>
        {GEN_STEPS[stepIndex]}… this can take up to a minute.
      </p>
    </div>
  );
}

export default function ResultStep({ form, status, errorMessage, result, onGenerate, onStartOver, onViewGallery }) {
  const assetUrl = result ? resolveAssetUrl(result.download_url) : null;
  const subLabel =
    getSubcategories(form.category).find((s) => s.value === form.targetAudience)?.label ||
    form.targetAudience;

  return (
    <>
      <div className="stage-head">
        <span className="stage-eyebrow">05 · Generate</span>
        <h1 className="stage-title">Ready when you are</h1>
        <p className="stage-sub">Double-check the summary, then generate. This usually takes under a minute.</p>
      </div>

      <div className="result-panel">
        {status !== "success" && (
          <ul className="summary-list">
            <li>
              <span>Studio</span>
              <strong>{form.studioType}</strong>
            </li>
            <li>
              <span>Category</span>
              <strong>{form.category}</strong>
            </li>
            <li>
              <span>Subcategory</span>
              <strong>{subLabel}</strong>
            </li>
            <li>
              <span>Model Region</span>
              <strong>{form.studioType === "Custom Model Studio" ? "Custom Upload" : form.region === "None" ? "No Model" : form.region}</strong>
            </li>
            <li>
              <span>Background</span>
              <strong>{form.background}</strong>
            </li>
            <li>
              <span>Style</span>
              <strong>{form.stylePreset}</strong>
            </li>
            <li>
              <span>Variations</span>
              <strong>{form.numImages}</strong>
            </li>
            <li>
              <span>Product</span>
              <strong>{form.productName || "—"}</strong>
            </li>
          </ul>
        )}

        {status === "idle" && (
          <button type="button" className="btn btn-primary" onClick={onGenerate}>
            Generate Now
          </button>
        )}

        {status === "loading" && <GenerationTimeline active />}

        {status === "error" && (
          <>
            <p className="error-text">{errorMessage}</p>
            <button type="button" className="btn btn-primary" onClick={onGenerate}>
              Try Again
            </button>
          </>
        )}

        {status === "success" && assetUrl && (
          <>
            <img className="result-image" src={assetUrl} alt="Generated result" />
            <div className="stage-nav" style={{ border: "none", width: "100%" }}>
              <a className="btn btn-ghost" href={assetUrl} download target="_blank" rel="noreferrer">
                Download Image
              </a>
              <div style={{ display: "flex", gap: "10px" }}>
                {onViewGallery && (
                  <button type="button" className="btn btn-ghost" onClick={onViewGallery}>
                    View in Gallery
                  </button>
                )}
                <button type="button" className="btn btn-primary" onClick={onStartOver}>
                  Start Over
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </>
  );
}