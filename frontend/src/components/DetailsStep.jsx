import React from "react";

export default function DetailsStep({ form, updateForm }) {
  return (
    <>
      <div className="stage-head">
        <span className="stage-eyebrow">04 · Add Details</span>
        <h1 className="stage-title">Tell us about the product</h1>
        <p className="stage-sub">
          This copy feeds directly into the prompt the AI uses, so the more specific, the better.
        </p>
      </div>

      <div className="field-group">
        <label className="field-label" htmlFor="productName">
          Product Name<span className="required">*</span>
        </label>
        <input
          id="productName"
          className="text-input"
          placeholder="Classic Cotton T-Shirt"
          value={form.productName}
          onChange={(e) => updateForm({ productName: e.target.value })}
          maxLength={120}
        />
      </div>

      <div className="field-group">
        <label className="field-label" htmlFor="brandName">
          Brand Name
        </label>
        <input
          id="brandName"
          className="text-input"
          placeholder="StyleCo"
          value={form.brandName}
          onChange={(e) => updateForm({ brandName: e.target.value })}
          maxLength={60}
        />
      </div>

      <div className="field-group">
        <label className="field-label" htmlFor="additionalInstructions">
          Additional Instructions
        </label>
        <textarea
          id="additionalInstructions"
          className="textarea-input"
          placeholder="Anything else the AI should know — lighting mood, props, pose direction..."
          value={form.additionalInstructions}
          onChange={(e) => updateForm({ additionalInstructions: e.target.value })}
          maxLength={200}
        />
        <span className="hint">{form.additionalInstructions.length}/200</span>
      </div>
    </>
  );
}