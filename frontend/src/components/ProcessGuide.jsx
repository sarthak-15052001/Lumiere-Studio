import { useState } from "react";

export default function ProcessGuide() {
  const [activeStep, setActiveStep] = useState(0);

  const steps = [
    {
      number: "01",
      title: "Upload Your Product",
      description: "Simply drag and drop or click to upload a clear photo of your product. Any format works — PNG, JPG, WEBP.",
      icon: "📸",
      details: [
        "✓ Works with any product category",
        "✓ No background removal needed",
        "✓ Supports up to 10MB files",
      ],
    },
    {
      number: "02",
      title: "Choose Your Studio",
      description: "Pick the vibe: Photo Studio for clean catalog shots, Marketing Studio for lifestyle scenes, or Custom Model Studio for your own model reference.",
      icon: "🎨",
      details: [
        "✓ Photo Studio: Crisp, clean backgrounds",
        "✓ Marketing Studio: Cinematic & dynamic",
        "✓ Custom Studio: Your model + your product",
      ],
    },
    {
      number: "03",
      title: "Customize Your Style",
      description: "Select backgrounds, lighting presets, model regions, and add custom instructions. Fine-tune every detail to match your brand.",
      icon: "⚙️",
      details: [
        "✓ 12+ background options",
        "✓ 6 style presets (Modern, Vintage, etc.)",
        "✓ Global model regions",
      ],
    },
    {
      number: "04",
      title: "Generate & Download",
      description: "Hit generate and wait 30-60 seconds for AI to create studio-quality images. Download instantly or save to your gallery.",
      icon: "✨",
      details: [
        "✓ Full-resolution PNG files",
        "✓ Ready for e-commerce platforms",
        "✓ Generate multiple variations",
      ],
    },
  ];

  return (
    <div className="process-guide">
      <div className="process-steps-vertical">
        {steps.map((step, idx) => (
          <div
            key={idx}
            className={`process-step-dot ${activeStep === idx ? "is-active" : ""} ${
              idx < activeStep ? "is-done" : ""
            }`}
            onClick={() => setActiveStep(idx)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") setActiveStep(idx);
            }}
          >
            <div className="process-step-dot-inner">
              {idx < activeStep ? "✓" : step.number.split("")[0]}
            </div>
          </div>
        ))}
      </div>

      <div className="process-steps-content">
        {steps.map((step, idx) => (
          <div
            key={idx}
            className={`process-step-panel ${activeStep === idx ? "is-active" : ""}`}
          >
            <div className="process-step-header">
              <div className="process-step-icon">{step.icon}</div>
              <div className="process-step-info">
                <span className="process-step-label">Step {step.number}</span>
                <h3 className="process-step-title">{step.title}</h3>
              </div>
            </div>

            <p className="process-step-description">{step.description}</p>

            <div className="process-step-details">
              <p className="process-step-details-label">What you get:</p>
              <ul className="process-step-details-list">
                {step.details.map((detail, i) => (
                  <li key={i}>{detail}</li>
                ))}
              </ul>
            </div>

            {/* Visual representation */}
            <div className="process-step-visual">
              {idx === 0 && (
                <div className="process-visual-mockup">
                  <div className="mockup-dropzone">
                    <div className="mockup-dropzone-icon">📤</div>
                    <p>Drag image here</p>
                  </div>
                </div>
              )}
              {idx === 1 && (
                <div className="process-visual-choices">
                  <div className="choice-pill">📦 Photo Studio</div>
                  <div className="choice-pill">🎬 Marketing</div>
                  <div className="choice-pill">👗 Custom Model</div>
                </div>
              )}
              {idx === 2 && (
                <div className="process-visual-customize">
                  <div className="customize-row">
                    <span className="customize-label">Background:</span>
                    <select className="customize-select">
                      <option>Solid White</option>
                      <option>Professional Studio</option>
                      <option>Urban</option>
                    </select>
                  </div>
                  <div className="customize-row">
                    <span className="customize-label">Style:</span>
                    <select className="customize-select">
                      <option>Modern</option>
                      <option>Vintage</option>
                      <option>Minimalist</option>
                    </select>
                  </div>
                </div>
              )}
              {idx === 3 && (
                <div className="process-visual-result">
                  <div className="result-box">
                    <div className="result-spinner">⏳</div>
                    <p>Generating...</p>
                  </div>
                  <div className="result-arrow">→</div>
                  <div className="result-box result-box-done">
                    <div className="result-image">✨</div>
                    <p>Ready!</p>
                  </div>
                </div>
              )}
            </div>

            <div className="process-step-actions">
              {idx > 0 && (
                <button
                  className="btn btn-ghost"
                  onClick={() => setActiveStep(idx - 1)}
                >
                  ← Previous
                </button>
              )}
              {idx < steps.length - 1 && (
                <button
                  className="btn btn-primary"
                  onClick={() => setActiveStep(idx + 1)}
                >
                  Next →
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}