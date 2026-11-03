import React, { useRef, useState } from "react";
import { getSubcategories } from "../config/categories.js";

const REGIONS = ["None", "Indian", "Western", "East Asian", "Middle Eastern"];

function formatSize(bytes) {
  if (!bytes) return "";
  const mb = bytes / (1024 * 1024);
  return `${mb.toFixed(1)} MB`;
}

function Dropzone({ label, file, onFile, accept = "image/*" }) {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped) onFile(dropped);
  };

  if (file) {
    return (
      <div className="preview-card">
        <img className="preview-thumb" src={URL.createObjectURL(file)} alt={`${label} preview`} />
        <div className="preview-meta">
          <span className="preview-name">{file.name}</span>
          <span className="preview-size">{formatSize(file.size)} · Ready</span>
        </div>
        <button type="button" className="btn btn-ghost" onClick={() => onFile(null)}>
          Replace
        </button>
      </div>
    );
  }

  return (
    <div
      className={`dropzone ${isDragging ? "is-dragging" : ""}`}
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      role="button"
      tabIndex={0}
    >
      <p className="dropzone-title">{label}</p>
      <p className="dropzone-sub">JPG, PNG, WEBP · up to 10MB</p>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        hidden
        onChange={(e) => onFile(e.target.files?.[0] || null)}
      />
    </div>
  );
}

export default function UploadStep({
  form,
  updateForm,
  isDualMode,
  file,
  setFile,
  ownImageFile,
  setOwnImageFile,
  productImageFile,
  setProductImageFile,
}) {
  const subLabel =
    getSubcategories(form.category).find((s) => s.value === form.targetAudience)?.label ||
    form.targetAudience;

  return (
    <>
      <div className="stage-head">
        <span className="stage-eyebrow">02 · Upload</span>
        <h1 className="stage-title">
          {isDualMode ? "Upload your model and product" : "Upload your product image"}
        </h1>
        <p className="stage-sub">
          {isDualMode
            ? "Custom Model Studio needs two photos: your model reference and the product itself."
            : `Shooting for ${subLabel}. A clear, well-lit photo of the product on its own works best.`}
        </p>
      </div>

      {isDualMode ? (
        <div className="upload-pair">
          <div className="field-group">
            <span className="field-label">Model Reference</span>
            <Dropzone label="Drop your model photo here" file={ownImageFile} onFile={setOwnImageFile} />
          </div>
          <div className="field-group">
            <span className="field-label">Product Photo</span>
            <Dropzone label="Drop your product photo here" file={productImageFile} onFile={setProductImageFile} />
          </div>
        </div>
      ) : (
        <div className="field-group">
          <span className="field-label">Product Photo</span>
          <Dropzone label="Drop your product image here" file={file} onFile={setFile} />
        </div>
      )}

      {/* Custom Model Studio supplies its own model in the upload above, so
          there's no AI model region to choose — this step is skipped for it,
          matching Arvora's flow. */}
      {!isDualMode && (
        <div className="field-group">
          <span className="field-label">Model Region</span>
          <p className="hint">
            "None" renders {form.category === "Fashion" ? "the garment" : "the product"} on its own,
            with no human model — useful for {form.targetAudience === "Jewelry" ? "jewellery display busts, " : ""}
            electronics, home decor, and other standalone product shots.
          </p>
          <div className="chip-row">
            {REGIONS.map((r) => (
              <button
                key={r}
                type="button"
                className={`chip ${form.region === r ? "is-selected" : ""}`}
                onClick={() => updateForm({ region: r })}
              >
                {r === "None" ? "No Model" : r}
              </button>
            ))}
          </div>
        </div>
      )}
    </>
  );
}