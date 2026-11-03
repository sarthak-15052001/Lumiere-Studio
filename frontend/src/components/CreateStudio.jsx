import React, { useState, useRef, useCallback, useMemo } from "react";
import { CATEGORIES, getSubcategories } from "../config/categories.js";
import { generateImage, generateDualImage } from "../api/client.js";
import photoStudioImg from "../asset/Photo-Studio.jpeg";
import marketingStudioImg from "../asset/marketing-studio.jpeg";
import customStudioImg from "../asset/custome-studio.jpeg";
import bgWhite from "../asset/white background.png";
import bgBlack from "../asset/solid black .png";
import bgIsolated from "../asset/Isoloted.jpeg";
import bgOffice from "../asset/office.jpeg";
import bgStudio from "../asset/professional studio.jpeg";
import bgCity from "../asset/city background.jpeg";
import bgHistoric from "../asset/historical.jpeg";
import bgHome from "../asset/home .jpeg";
import bgCustom from "../asset/custom.jpeg";
import apparelProfessional from "../asset/professional styel.jpeg";
import apparelCasual from "../asset/casual.jpeg";

/* ── Studio Types ──────────────────────────────────────── */
const STUDIO_TYPES = [
  {
    value: "Photo Studio",
    title: "Photo Studio",
    desc: "Clean, high-conversion catalog shots with plain product backdrops and crisp detail.",
    image: photoStudioImg,
    badge: "Catalog",
  },
  {
    value: "Marketing Studio",
    title: "Marketing Studio",
    desc: "Dynamic campaign visuals and social media content built for ads and storytelling.",
    image: marketingStudioImg,
    badge: "Campaign",
  },
  {
    value: "Custom Model Studio",
    title: "Custom Model Studio",
    desc: "Upload your own model reference photo and let AI blend your product onto it naturally.",
    image: customStudioImg,
    badge: "Personalized",
  },
];

const REGIONS = ["None", "Indian", "Western", "East Asian", "Middle Eastern"];
const BACKGROUNDS = [
  { label: "Solid White", image: bgWhite },
  { label: "Solid Black", image: bgBlack },
  { label: "Isolated", image: bgIsolated },
  { label: "Office", image: bgOffice },
  { label: "Professional Studio", image: bgStudio },
  { label: "City", image: bgCity },
  { label: "Historic", image: bgHistoric },
  { label: "HomeVibe", image: bgHome },
  { label: "Custom Idea", image: bgCustom },
];
const STYLE_PRESETS = ["Modern", "Minimalist", "Vintage", "Monochrome", "Aesthetic", "Close-up"];
const APPAREL_STYLES = [
  { label: "Professional", image: apparelProfessional },
  { label: "Casual", image: apparelCasual },
];

/* ── Reliable Unsplash images (tested working) ──────────── */
const CATEGORY_IMAGES = {
  Fashion: "https://images.unsplash.com/photo-1445205170230-053b83016050?w=600&h=400&fit=crop",
  Accessories: "https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=600&h=400&fit=crop",
  "E-commerce": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&h=400&fit=crop",
};

const SUBCATEGORY_IMAGES = {
  Women: "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=600&h=400&fit=crop",
  Men: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop",
  Kids: "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=600&h=400&fit=crop",
  "Bags & Purses": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&h=400&fit=crop",
  Jewelry: "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&h=400&fit=crop",
  Watches: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=600&h=400&fit=crop",
  "Home Decor": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&h=400&fit=crop",
  Electronics: "https://images.unsplash.com/photo-1468495244123-6c6c332eeece?w=600&h=400&fit=crop",
  Other: "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=600&h=400&fit=crop",
};

const REGION_ICONS = {
  None: "🚫",
  Indian: "🇮🇳",
  Western: "🇺🇸",
  "East Asian": "🇯🇵",
  "Middle Eastern": "🇦🇪",
};

/* ── Utility ───────────────────────────────────────────── */
function formatSize(bytes) {
  if (!bytes) return "";
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

/* ── Section Wrapper ───────────────────────────────────── */
function Section({ number, title, subtitle, visible, children }) {
  if (!visible) return null;
  return (
    <div className="cs-section cs-anim-slide-up">
      <div className="cs-section-header">
        <div className="cs-section-number">{number}</div>
        <div>
          <h2 className="cs-section-title">{title}</h2>
          <p className="cs-section-subtitle">{subtitle}</p>
        </div>
      </div>
      {children}
    </div>
  );
}

/* ── Main Component ────────────────────────────────────── */
export default function CreateStudio({ onStartOver: onReset, onViewGallery }) {
  /* ── State ─────────────────────────────────────────────── */
  const [studioType, setStudioType] = useState(null);
  const [category, setCategory] = useState(null);
  const [targetAudience, setTargetAudience] = useState(null);
  const [region, setRegion] = useState("Indian");
  const [files, setFiles] = useState([]);
  const [ownImageFile, setOwnImageFile] = useState(null);
  const [productImageFile, setProductImageFile] = useState(null);
  const [stylePreset, setStylePreset] = useState(null);
  const [background, setBackground] = useState(null);
  const [customBackground, setCustomBackground] = useState("");
  const [apparelStyle, setApparelStyle] = useState(null);
  const [productName, setProductName] = useState("");
  const [brandName, setBrandName] = useState("");
  const [additionalInstructions, setAdditionalInstructions] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [dragTarget, setDragTarget] = useState(null);
  const [status, setStatus] = useState("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const [result, setResult] = useState(null);

  /* ── Separate file inputs for dual mode ────────────────── */
  const modelInputRef = useRef(null);
  const productInputRef = useRef(null);
  const singleInputRef = useRef(null);

  const isDualMode = studioType === "Custom Model Studio";

  /* ── Derived ────────────────────────────────────────────── */
  const subcategories = useMemo(() => {
    if (!category) return [];
    return getSubcategories(category);
  }, [category]);

  /* ── Selection handlers ─────────────────────────────────── */
  const handleStudioSelect = (value) => {
    setStudioType(value);
    setCategory(null);
    setTargetAudience(null);
  };

  const handleCategorySelect = (value) => {
    setCategory(value);
    const firstSub = getSubcategories(value)[0];
    setTargetAudience(firstSub.value);
    setRegion(firstSub.defaultRegion);
  };

  const handleSubcategorySelect = (sub) => {
    setTargetAudience(sub.value);
    if (!isDualMode) setRegion(sub.defaultRegion);
  };

  /* ── File handling ──────────────────────────────────────── */
  const addFiles = useCallback((newFiles) => {
    const arr = Array.from(newFiles)
      .filter((f) => f.type.startsWith("image/"))
      .slice(0, 10);
    setFiles((prev) => [...prev, ...arr].slice(0, 10));
  }, []);

  const removeFile = (idx) => {
    setFiles((prev) => prev.filter((_, i) => i !== idx));
  };

  const handleSingleDragOver = (e) => { e.preventDefault(); setIsDragging(true); setDragTarget("single"); };
  const handleSingleDragLeave = (e) => { e.preventDefault(); setIsDragging(false); setDragTarget(null); };
  const handleSingleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    setDragTarget(null);
    addFiles(e.dataTransfer.files);
  };

  const handleModelDragOver = (e) => { e.preventDefault(); setIsDragging(true); setDragTarget("model"); };
  const handleModelDragLeave = (e) => { e.preventDefault(); setIsDragging(false); setDragTarget(null); };
  const handleModelDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    setDragTarget(null);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped && dropped.type.startsWith("image/")) setOwnImageFile(dropped);
  };

  const handleProductDragOver = (e) => { e.preventDefault(); setIsDragging(true); setDragTarget("product"); };
  const handleProductDragLeave = (e) => { e.preventDefault(); setIsDragging(false); setDragTarget(null); };
  const handleProductDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    setDragTarget(null);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped && dropped.type.startsWith("image/")) setProductImageFile(dropped);
  };

  /* ── Generate ────────────────────────────────────────────── */
  const handleGenerate = async () => {
    setStatus("loading");
    setErrorMessage("");
    try {
      const formValues = {
        studioType, category, targetAudience, region,
        stylePreset, background, customBackground, apparelStyle,
        numImages: 1, productName, brandName, additionalInstructions,
      };
      const data = isDualMode
        ? await generateDualImage(formValues, ownImageFile, productImageFile)
        : await generateImage(formValues, files[0]);
      setResult(data);
      setStatus("success");
    } catch (err) {
      setErrorMessage(
        err?.response?.data?.detail || err?.message || "Something went wrong while generating."
      );
      setStatus("error");
    }
  };

  const handleStartOver = () => {
    setStudioType(null);
    setCategory(null);
    setTargetAudience(null);
    setRegion("Indian");
    setFiles([]);
    setOwnImageFile(null);
    setProductImageFile(null);
    setStylePreset(null);
    setBackground(null);
    setCustomBackground("");
    setApparelStyle(null);
    setProductName("");
    setBrandName("");
    setAdditionalInstructions("");
    setStatus("idle");
    setResult(null);
    setErrorMessage("");
  };

  /* ── Summary items ──────────────────────────────────────── */
  const summaryItems = useMemo(() => [
    { label: "Studio", value: studioType, completed: !!studioType },
    { label: "Category", value: category, completed: !!category },
    { label: "Subcategory", value: targetAudience, completed: !!targetAudience },
    { label: "Images", value: isDualMode
      ? (ownImageFile && productImageFile ? "2 uploaded" : null)
      : (files.length > 0 ? `${files.length} uploaded` : null),
      completed: isDualMode ? !!(ownImageFile && productImageFile) : files.length > 0,
    },
    { label: "Model Region", value: isDualMode ? "Custom Upload" : region, completed: true },
    { label: "Style", value: stylePreset, completed: !!stylePreset },
    { label: "Background", value: background, completed: !!background },
    { label: "Apparel", value: apparelStyle, completed: !!apparelStyle },
    { label: "Product", value: productName || null, completed: !!productName.trim() },
  ], [studioType, category, targetAudience, files, isDualMode, ownImageFile, productImageFile, region, stylePreset, background, apparelStyle, productName]);

  const completedCount = summaryItems.filter((i) => i.completed).length;

  /* ── Render ─────────────────────────────────────────────── */
  return (
    <div className="cs-layout">
      {/* ── Left: Workflow ─────────────────────────────── */}
      <div className="cs-workflow">

        {/* Step 1: Choose Studio */}
        <Section
          number={1}
          title="Choose Studio"
          subtitle="Select the studio type that best fits your product photography needs."
          visible={true}
        >
          <div className="cs-studio-grid">
            {STUDIO_TYPES.map((s) => (
              <button
                key={s.value}
                type="button"
                className={`cs-studio-card ${studioType === s.value ? "cs-selected" : ""}`}
                onClick={() => handleStudioSelect(s.value)}
              >
                <div className="cs-studio-card-visual">
                  <img src={s.image} alt={s.title} className="cs-studio-card-img" />
                  <div className="cs-studio-card-overlay" />
                </div>
                <div className="cs-studio-card-body">
                  <div className="cs-studio-card-top">
                    <h3 className="cs-studio-card-title">{s.title}</h3>
                    <span className="cs-studio-card-badge">{s.badge}</span>
                  </div>
                  <p className="cs-studio-card-desc">{s.desc}</p>
                </div>
                {studioType === s.value && <div className="cs-check-badge">✓</div>}
              </button>
            ))}
          </div>
        </Section>

        {/* Step 2: Choose Category */}
        <Section
          number={2}
          title="Choose Category"
          subtitle="Pick the product category for your photoshoot."
          visible={!!studioType}
        >
          <div className="cs-image-grid">
            {CATEGORIES.map((c) => (
              <button
                key={c.value}
                type="button"
                className={`cs-image-card ${category === c.value ? "cs-selected" : ""}`}
                onClick={() => handleCategorySelect(c.value)}
              >
                <div className="cs-image-card-img-wrap">
                  <img src={CATEGORY_IMAGES[c.value]} alt={c.label} className="cs-image-card-img" loading="lazy" />
                  <div className="cs-image-card-overlay" />
                </div>
                <div className="cs-image-card-body">
                  <span className="cs-image-card-title">{c.label}</span>
                  {category === c.value && <span className="cs-check-dot">✓</span>}
                </div>
              </button>
            ))}
          </div>
        </Section>

        {/* Step 3: Choose Subcategory */}
        <Section
          number={3}
          title="Choose Subcategory"
          subtitle="Narrow down your product type for more precise results."
          visible={!!category}
        >
          <div className="cs-image-grid">
            {subcategories.map((sub) => (
              <button
                key={sub.value}
                type="button"
                className={`cs-image-card ${targetAudience === sub.value ? "cs-selected" : ""}`}
                onClick={() => handleSubcategorySelect(sub)}
              >
                <div className="cs-image-card-img-wrap">
                  <img src={SUBCATEGORY_IMAGES[sub.value]} alt={sub.label} className="cs-image-card-img" loading="lazy" />
                  <div className="cs-image-card-overlay" />
                </div>
                <div className="cs-image-card-body">
                  <span className="cs-image-card-title">{sub.label}</span>
                  {targetAudience === sub.value && <span className="cs-check-dot">✓</span>}
                </div>
              </button>
            ))}
          </div>
        </Section>

        {/* Step 4: Upload Images + Region */}
        <Section
          number={4}
          title="Upload Images"
          subtitle={isDualMode ? "Upload your model reference and product photo." : "Upload your product image. Drag & drop or click to browse."}
          visible={!!targetAudience}
        >
          {isDualMode ? (
            <div className="cs-upload-pair">
              {/* Model Reference */}
              <div className="cs-field-group">
                <span className="cs-field-label">Model Reference</span>
                <div
                  className={`cs-dropzone ${isDragging && dragTarget === "model" ? "cs-dragging" : ""}`}
                  onDragOver={handleModelDragOver}
                  onDragLeave={handleModelDragLeave}
                  onDrop={handleModelDrop}
                  onClick={() => !ownImageFile && modelInputRef.current?.click()}
                >
                  {ownImageFile ? (
                    <div className="cs-preview-card">
                      <img className="cs-preview-thumb" src={URL.createObjectURL(ownImageFile)} alt="Model preview" />
                      <div className="cs-preview-meta">
                        <span className="cs-preview-name">{ownImageFile.name}</span>
                        <span className="cs-preview-size">{formatSize(ownImageFile.size)} · Ready</span>
                      </div>
                      <button type="button" className="cs-btn-remove" onClick={(e) => { e.stopPropagation(); setOwnImageFile(null); }}>✕</button>
                    </div>
                  ) : (
                    <>
                      <div className="cs-dropzone-icon">📸</div>
                      <p className="cs-dropzone-title">Drop your model photo here</p>
                      <p className="cs-dropzone-sub">JPG, PNG, WEBP · up to 10MB</p>
                    </>
                  )}
                  <input
                    ref={modelInputRef}
                    type="file"
                    accept="image/*"
                    hidden
                    onChange={(e) => {
                      const f = e.target.files?.[0];
                      if (f) setOwnImageFile(f);
                      e.target.value = "";
                    }}
                  />
                </div>
              </div>
              {/* Product Photo */}
              <div className="cs-field-group">
                <span className="cs-field-label">Product Photo</span>
                <div
                  className={`cs-dropzone ${isDragging && dragTarget === "product" ? "cs-dragging" : ""}`}
                  onDragOver={handleProductDragOver}
                  onDragLeave={handleProductDragLeave}
                  onDrop={handleProductDrop}
                  onClick={() => !productImageFile && productInputRef.current?.click()}
                >
                  {productImageFile ? (
                    <div className="cs-preview-card">
                      <img className="cs-preview-thumb" src={URL.createObjectURL(productImageFile)} alt="Product preview" />
                      <div className="cs-preview-meta">
                        <span className="cs-preview-name">{productImageFile.name}</span>
                        <span className="cs-preview-size">{formatSize(productImageFile.size)} · Ready</span>
                      </div>
                      <button type="button" className="cs-btn-remove" onClick={(e) => { e.stopPropagation(); setProductImageFile(null); }}>✕</button>
                    </div>
                  ) : (
                    <>
                      <div className="cs-dropzone-icon">📦</div>
                      <p className="cs-dropzone-title">Drop your product photo here</p>
                      <p className="cs-dropzone-sub">JPG, PNG, WEBP · up to 10MB</p>
                    </>
                  )}
                  <input
                    ref={productInputRef}
                    type="file"
                    accept="image/*"
                    hidden
                    onChange={(e) => {
                      const f = e.target.files?.[0];
                      if (f) setProductImageFile(f);
                      e.target.value = "";
                    }}
                  />
                </div>
              </div>
            </div>
          ) : (
            <div className="cs-field-group">
              <div
                className={`cs-dropzone ${isDragging && dragTarget === "single" ? "cs-dragging" : ""}`}
                onDragOver={handleSingleDragOver}
                onDragLeave={handleSingleDragLeave}
                onDrop={handleSingleDrop}
                onClick={() => singleInputRef.current?.click()}
              >
                {files.length === 0 ? (
                  <>
                    <div className="cs-dropzone-icon">📁</div>
                    <p className="cs-dropzone-title">Drop your product images here</p>
                    <p className="cs-dropzone-sub">JPG, PNG, WEBP · up to 10MB each · Max 10 images</p>
                  </>
                ) : (
                  <div className="cs-dropzone-has-files">
                    <p className="cs-dropzone-title">{files.length} image{files.length > 1 ? "s" : ""} selected</p>
                    <p className="cs-dropzone-sub">Click or drop to add more</p>
                  </div>
                )}
                <input
                  ref={singleInputRef}
                  type="file"
                  multiple
                  accept="image/*"
                  hidden
                  onChange={(e) => { if (e.target.files) addFiles(e.target.files); e.target.value = ""; }}
                />
              </div>
              {files.length > 0 && (
                <div className="cs-file-list">
                  {files.map((f, idx) => (
                    <div key={idx} className="cs-file-item">
                      <img className="cs-file-thumb" src={URL.createObjectURL(f)} alt={f.name} />
                      <div className="cs-file-meta">
                        <span className="cs-file-name">{f.name}</span>
                        <span className="cs-file-size">{formatSize(f.size)}</span>
                      </div>
                      <button type="button" className="cs-btn-remove" onClick={() => removeFile(idx)}>✕</button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Model Region — only for non-dual mode */}
          {!isDualMode && (
            <div className="cs-field-group">
              <span className="cs-field-label">Model Region</span>
              <p className="cs-hint">
                "None" renders the product on its own, with no human model.
              </p>
              <div className="cs-chip-row">
                {REGIONS.map((r) => (
                  <button
                    key={r}
                    type="button"
                    className={`cs-chip ${region === r ? "cs-selected" : ""}`}
                    onClick={() => setRegion(r)}
                  >
                    <span className="cs-chip-icon">{REGION_ICONS[r]}</span>
                    {r === "None" ? "No Model" : r}
                  </button>
                ))}
              </div>
            </div>
          )}
        </Section>

        {/* Step 5: Select Style */}
        <Section
          number={5}
          title="Select Style"
          subtitle="Pick a style preset and apparel style for your generated images."
          visible={isDualMode ? !!(ownImageFile && productImageFile) : files.length > 0}
        >
          <div className="cs-field-group">
            <span className="cs-field-label">Style Preset</span>
            <div className="cs-chip-row">
              {STYLE_PRESETS.map((s) => (
                <button
                  key={s}
                  type="button"
                  className={`cs-chip ${stylePreset === s ? "cs-selected" : ""}`}
                  onClick={() => setStylePreset(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          <div className="cs-field-group">
            <span className="cs-field-label">Apparel Style</span>
            <div className="cs-bg-grid">
              {APPAREL_STYLES.map((s) => (
                <button
                  key={s.label}
                  type="button"
                  className={`cs-bg-card ${apparelStyle === s.label ? "cs-selected" : ""}`}
                  onClick={() => setApparelStyle(s.label)}
                >
                  <div className="cs-bg-img-wrap">
                    <img src={s.image} alt={s.label} className="cs-bg-img" loading="lazy" />
                  </div>
                  <span className="cs-bg-label">{s.label}</span>
                  {apparelStyle === s.label && <div className="cs-check-badge-sm">✓</div>}
                </button>
              ))}
            </div>
          </div>
        </Section>

        {/* Step 6: Select Background */}
        <Section
          number={6}
          title="Select Background"
          subtitle="Choose a background for your product images."
          visible={!!stylePreset}
        >
          <div className="cs-bg-grid">
            {BACKGROUNDS.map((b) => (
              <button
                key={b.label}
                type="button"
                className={`cs-bg-card ${background === b.label ? "cs-selected" : ""}`}
                onClick={() => setBackground(b.label)}
              >
                <div className="cs-bg-img-wrap">
                  <img src={b.image} alt={b.label} className="cs-bg-img" loading="lazy" />
                </div>
                <span className="cs-bg-label">{b.label}</span>
                {background === b.label && <div className="cs-check-badge-sm">✓</div>}
              </button>
            ))}
          </div>
          {background === "Custom Idea" && (
            <div className="cs-field-group">
              <input
                className="cs-text-input"
                placeholder="Describe the background you have in mind..."
                value={customBackground}
                onChange={(e) => setCustomBackground(e.target.value)}
                maxLength={150}
              />
              <span className="cs-char-count">{customBackground.length} / 150 characters</span>
            </div>
          )}
        </Section>

        {/* Step 7: Additional Details + Generate */}
        <Section
          number={7}
          title="Add Details"
          subtitle="Enter product details and any custom instructions for the AI generation."
          visible={!!background && (background !== "Custom Idea" || customBackground.trim())}
        >
          <div className="cs-details-grid">
            <div className="cs-field-group">
              <label className="cs-field-label" htmlFor="cs-product-name">
                Product Name <span className="cs-required">*</span>
              </label>
              <input
                id="cs-product-name"
                className="cs-text-input"
                placeholder="Classic Cotton T-Shirt"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                maxLength={120}
              />
            </div>
            <div className="cs-field-group">
              <label className="cs-field-label" htmlFor="cs-brand-name">
                Brand Name
              </label>
              <input
                id="cs-brand-name"
                className="cs-text-input"
                placeholder="StyleCo"
                value={brandName}
                onChange={(e) => setBrandName(e.target.value)}
                maxLength={60}
              />
            </div>
          </div>

          <div className="cs-field-group">
            <label className="cs-field-label" htmlFor="cs-instructions">
              Additional Instructions
            </label>
            <textarea
              id="cs-instructions"
              className="cs-textarea"
              placeholder="Anything else the AI should know — lighting mood, props, pose direction..."
              value={additionalInstructions}
              onChange={(e) => setAdditionalInstructions(e.target.value)}
              maxLength={200}
              rows={4}
            />
            <span className="cs-hint">{additionalInstructions.length}/200</span>
          </div>

          {/* Generate */}
          {productName.trim() && (
            <div className="cs-generate-section">
              {status === "idle" && (
                <button type="button" className="cs-generate-btn" onClick={handleGenerate}>
                  <span>✨</span> Generate Now
                </button>
              )}
              {status === "loading" && (
                <div className="cs-loading">
                  <div className="cs-spinner" />
                  <p>Generating your images... this can take up to a minute.</p>
                </div>
              )}
              {status === "error" && (
                <div className="cs-error">
                  <p>{errorMessage}</p>
                  <button type="button" className="cs-generate-btn" onClick={handleGenerate}>
                    Try Again
                  </button>
                </div>
              )}
              {status === "success" && result && (
                <div className="cs-result">
                  <img
                    className="cs-result-image"
                    src={result.download_url}
                    alt="Generated result"
                  />
                  <div className="cs-result-actions">
                    <a className="cs-btn cs-btn-ghost" href={result.download_url} download target="_blank" rel="noreferrer">
                      Download
                    </a>
                    {onViewGallery && (
                      <button type="button" className="cs-btn cs-btn-ghost" onClick={onViewGallery}>
                        View Gallery
                      </button>
                    )}
                    <button type="button" className="cs-btn cs-btn-primary" onClick={handleStartOver}>
                      Start Over
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}
        </Section>
      </div>

      {/* ── Right: Sticky Summary Panel ────────────────── */}
      <aside className="cs-summary">
        <div className="cs-summary-inner">
          <div className="cs-summary-header">
            <h3 className="cs-summary-title">Summary</h3>
            <span className="cs-summary-count">{completedCount}/{summaryItems.length}</span>
          </div>

          <div className="cs-summary-progress">
            <div
              className="cs-summary-progress-bar"
              style={{ width: `${(completedCount / summaryItems.length) * 100}%` }}
            />
          </div>

          <div className="cs-summary-items">
            {summaryItems.map((item, idx) => (
              <div
                key={item.label}
                className={`cs-summary-item ${item.completed ? "cs-done" : ""}`}
              >
                <div className={`cs-summary-dot ${item.completed ? "cs-done" : ""}`}>
                  {item.completed ? "✓" : idx + 1}
                </div>
                <div className="cs-summary-content">
                  <span className="cs-summary-label">{item.label}</span>
                  <span className="cs-summary-value">
                    {item.value || <span className="cs-summary-pending">Pending</span>}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {studioType && (
            <button type="button" className="cs-btn cs-btn-ghost cs-btn-full" onClick={handleStartOver} style={{ marginTop: 16 }}>
              Start Over
            </button>
          )}
        </div>
      </aside>
    </div>
  );
}
