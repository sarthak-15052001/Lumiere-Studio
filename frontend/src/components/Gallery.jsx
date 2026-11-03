import React, { useEffect, useMemo, useState, useCallback, useRef } from "react";
import { getGallery } from "../api/client.js";

const NEW_WINDOW_SECONDS = 24 * 60 * 60;

function formatSize(bytes) {
  if (!bytes && bytes !== 0) return "";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(unixSeconds) {
  if (!unixSeconds) return "";
  return new Date(unixSeconds * 1000).toLocaleString(undefined, {
    day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit",
  });
}

function timeAgo(unixSeconds) {
  if (!unixSeconds) return "";
  const diff = Date.now() / 1000 - unixSeconds;
  if (diff < 60) return "just now";
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

function toDisplayName(img) {
  if (img.product_name && img.product_name.trim()) return img.product_name.trim();
  const base = img.filename.replace(/\.[^/.]+$/, "");
  if (/^[a-f0-9-]{16,}$/i.test(base)) return "Generated Image";
  return base.replace(/[-_]+/g, " ").replace(/\s+/g, " ").trim().replace(/\b\w/g, (c) => c.toUpperCase());
}

const FILTER_OPTIONS = ["All"];

export default function Gallery({ onUseAsReference }) {
  const [images, setImages] = useState([]);
  const [status, setStatus] = useState("loading");
  const [errorMessage, setErrorMessage] = useState("");
  const [query, setQuery] = useState("");
  const [activeFilter, setActiveFilter] = useState("All");
  const [activeImage, setActiveImage] = useState(null);
  const [copiedFilename, setCopiedFilename] = useState(null);
  const [viewMode, setViewMode] = useState("grid"); // grid | list
  const copiedTimeoutRef = useRef(null);

  const loadGallery = useCallback(async () => {
    setStatus("loading");
    setErrorMessage("");
    try {
      const data = await getGallery();
      setImages(data);
      setStatus("success");
    } catch (err) {
      setErrorMessage(err?.response?.data?.detail || err?.message || "Couldn't load the gallery.");
      setStatus("error");
    }
  }, []);

  useEffect(() => { loadGallery(); }, [loadGallery]);

  useEffect(() => {
    if (!activeImage) return;
    const onKeyDown = (e) => { if (e.key === "Escape") setActiveImage(null); };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [activeImage]);

  useEffect(() => () => clearTimeout(copiedTimeoutRef.current), []);

  const filteredImages = useMemo(() => {
    let result = images;
    if (activeFilter !== "All") {
      result = result.filter((img) => img.category === activeFilter);
    }
    const q = query.trim().toLowerCase();
    if (q) {
      result = result.filter((img) => {
        const haystack = [img.product_name, img.brand_name, img.category, img.filename]
          .filter(Boolean).join(" ").toLowerCase();
        return haystack.includes(q);
      });
    }
    return result;
  }, [images, query, activeFilter]);

  const recentImages = useMemo(() => images.slice(0, 8), [images]);

  const handleDownload = async (img, e) => {
    e?.stopPropagation();
    try {
      const response = await fetch(img.url);
      const blob = await response.blob();
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = blobUrl;
      a.download = img.filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(blobUrl);
    } catch {
      window.open(img.url, "_blank", "noreferrer");
    }
  };

  const handleCopyLink = async (img, e) => {
    e?.stopPropagation();
    try {
      await navigator.clipboard.writeText(img.url);
    } catch {
      window.prompt("Copy this link:", img.url);
    }
    setCopiedFilename(img.filename);
    clearTimeout(copiedTimeoutRef.current);
    copiedTimeoutRef.current = setTimeout(() => setCopiedFilename(null), 1600);
  };

  const handleUseAsRef = (img, e) => {
    e?.stopPropagation();
    onUseAsReference?.(img);
  };

  const nowSeconds = Date.now() / 1000;

  return (
    <>
      {/* Header */}
      <div className="stage-head">
        <span className="stage-eyebrow">Gallery</span>
        <h1 className="stage-title">Your Generated Images</h1>
        <p className="stage-sub">
          Browse, download, or use your generated images as a reference for your next creation.
        </p>
      </div>

      {/* Stats bar */}
      {status === "success" && images.length > 0 && (
        <div className="gallery-stats">
          <div className="gallery-stat-item">
            <span className="gallery-stat-num">{images.length}</span>
            <span className="gallery-stat-label">Total Images</span>
          </div>
          <div className="gallery-stat-item">
            <span className="gallery-stat-num">{images.filter((i) => nowSeconds - i.created_at < NEW_WINDOW_SECONDS).length}</span>
            <span className="gallery-stat-label">New Today</span>
          </div>
          {/* <div className="gallery-stat-item">
            <span className="gallery-stat-num">{[...new Set(images.map((i) => i.category).filter(Boolean))].length}</span>
            <span className="gallery-stat-label">Categories</span>
          </div> */}
        </div>
      )}

      {/* Recent Activity Timeline */}
      {recentImages.length > 0 && (
        <div className="gen-timeline">
          <span className="gen-timeline-label">Recent Activity</span>
          <ul className="gen-timeline-rail">
            {recentImages.map((img, idx) => (
              <li className="gen-timeline-item" key={img.filename}>
                <button
                  type="button"
                  className="gen-timeline-thumb"
                  onClick={() => setActiveImage(img)}
                  title={toDisplayName(img)}
                >
                  <img src={img.url} alt={toDisplayName(img)} loading="lazy" />
                </button>
                <span className="gen-timeline-time">{timeAgo(img.created_at)}</span>
                {idx < recentImages.length - 1 && <span className="gen-timeline-connector" />}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Toolbar */}
      <div className="gallery-toolbar">
        <input
          type="text"
          className="text-input gallery-search"
          placeholder="Search by product, brand, category..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        {/* <div className="gallery-toolbar-right">
          <div className="chip-row">
            {FILTER_OPTIONS.map((f) => (
              <button
                key={f}
                type="button"
                className={`chip ${activeFilter === f ? "is-selected" : ""}`}
                onClick={() => setActiveFilter(f)}
              >
                {f}
              </button>
            ))}
          </div>
          <div className="gallery-view-toggle">
            <button
              type="button"
              className={`gallery-view-btn ${viewMode === "grid" ? "is-active" : ""}`}
              onClick={() => setViewMode("grid")}
              title="Grid view"
            >
              ⧉
            </button>
            <button
              type="button"
              className={`gallery-view-btn ${viewMode === "list" ? "is-active" : ""}`}
              onClick={() => setViewMode("list")}
              title="List view"
            >
              ☰
            </button>
          </div>
          <button type="button" className="btn btn-ghost" onClick={loadGallery} disabled={status === "loading"}>
            {status === "loading" ? "Refreshing…" : "↻ Refresh"}
          </button>
        </div> */}
      </div>

      {/* Count */}
      {status === "success" && (
        <p className="hint">
          Showing {filteredImages.length} of {images.length} image{images.length === 1 ? "" : "s"}
          {activeFilter !== "All" ? ` in ${activeFilter}` : ""}
        </p>
      )}

      {/* States */}
      {status === "loading" && images.length === 0 && (
        <div className="result-panel">
          <div className="spinner" role="status" aria-label="Loading gallery" />
          <p className="hint">Loading your generated images…</p>
        </div>
      )}

      {status === "error" && (
        <div className="result-panel">
          <p className="error-text">{errorMessage}</p>
          <button type="button" className="btn btn-primary" onClick={loadGallery}>Try Again</button>
        </div>
      )}

      {status === "success" && images.length === 0 && (
        <div className="gallery-empty">
          <div className="gallery-empty-icon">🎨</div>
          <h3 className="gallery-empty-title">No images yet</h3>
          <p className="gallery-empty-sub">Generate something in the Studio and it'll appear here.</p>
        </div>
      )}

      {status === "success" && images.length > 0 && filteredImages.length === 0 && (
        <div className="gallery-empty">
          <div className="gallery-empty-icon">🔍</div>
          <h3 className="gallery-empty-title">No results found</h3>
          <p className="gallery-empty-sub">Try a different search term or filter.</p>
        </div>
      )}

      {/* Grid */}
      {filteredImages.length > 0 && (
        <div className={viewMode === "grid" ? "gallery-grid" : "gallery-list"}>
          {filteredImages.map((img) => {
            const isNew = nowSeconds - img.created_at < NEW_WINDOW_SECONDS;
            return viewMode === "grid" ? (
              <div className="gallery-card" key={img.filename}>
                <div className="gallery-card-frame">
                  {isNew && <span className="gallery-card-badge">New</span>}
                  <img
                    src={img.url}
                    alt={toDisplayName(img)}
                    loading="lazy"
                    onClick={() => setActiveImage(img)}
                  />
                </div>
                <div className="gallery-card-body">
                  <h4 className="gallery-card-title">{toDisplayName(img)}</h4>
                  {img.brand_name && (
                    <p className="gallery-card-meta">Brand: {img.brand_name}</p>
                  )}
                  {img.category && (
                    <p className="gallery-card-meta">Category: {img.category}</p>
                  )}
                  <p className="gallery-card-meta hint">
                    {formatSize(img.size_bytes)} • {formatDate(img.created_at)}
                  </p>
                  <div className="gallery-card-actions">
                    <button
                      type="button"
                      className="gallery-action-btn"
                      onClick={(e) => handleDownload(img, e)}
                      title="Download image"
                    >
                      ↓ Download
                    </button>
                    <button
                      type="button"
                      className="gallery-action-btn"
                      onClick={(e) => handleCopyLink(img, e)}
                      title="Copy image URL"
                    >
                      {copiedFilename === img.filename ? "✓ Copied" : "🔗 Copy"}
                    </button>
                    {onUseAsReference && (
                      <button
                        type="button"
                        className="gallery-action-btn"
                        onClick={(e) => handleUseAsRef(img, e)}
                        title="Use as reference in Custom Model Studio"
                      >
                        📌 Use as Ref
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <div className="gallery-list-item" key={img.filename}>
                <div className="gallery-list-thumbnail">
                  {isNew && <span className="gallery-card-badge">New</span>}
                  <img
                    src={img.url}
                    alt={toDisplayName(img)}
                    loading="lazy"
                    onClick={() => setActiveImage(img)}
                  />
                </div>
                <div className="gallery-list-info">
                  <h4 className="gallery-list-title" onClick={() => setActiveImage(img)}>
                    {toDisplayName(img)}
                  </h4>
                  <div className="gallery-list-details">
                    {img.brand_name && (
                      <span className="gallery-list-meta">Brand: {img.brand_name}</span>
                    )}
                    {img.category && (
                      <span className="gallery-list-meta">Category: {img.category}</span>
                    )}
                    <span className="gallery-list-meta">{formatSize(img.size_bytes)}</span>
                    <span className="gallery-list-meta hint">{formatDate(img.created_at)}</span>
                  </div>
                </div>
                <div className="gallery-list-actions">
                  <button
                    type="button"
                    className="gallery-action-btn"
                    onClick={(e) => handleDownload(img, e)}
                    title="Download"
                  >
                    ↓
                  </button>
                  <button
                    type="button"
                    className="gallery-action-btn"
                    onClick={(e) => handleCopyLink(img, e)}
                    title="Copy URL"
                  >
                    {copiedFilename === img.filename ? "✓" : "🔗"}
                  </button>
                  {onUseAsReference && (
                    <button
                      type="button"
                      className="gallery-action-btn"
                      onClick={(e) => handleUseAsRef(img, e)}
                      title="Use as reference"
                    >
                      📌
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Lightbox / Modal */}
      {activeImage && (
        <div className="modal-overlay" onClick={() => setActiveImage(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button
              type="button"
              className="modal-close"
              onClick={() => setActiveImage(null)}
              aria-label="Close modal"
            >
              ✕
            </button>
            <div className="modal-body">
              <img
                src={activeImage.url}
                alt={toDisplayName(activeImage)}
                className="modal-image"
              />
            </div>
            <div className="modal-footer">
              <div className="modal-info">
                <h3 className="modal-title">{toDisplayName(activeImage)}</h3>
                {activeImage.brand_name && (
                  <p className="modal-meta">Brand: {activeImage.brand_name}</p>
                )}
                {activeImage.category && (
                  <p className="modal-meta">Category: {activeImage.category}</p>
                )}
                <p className="modal-meta hint">
                  {formatSize(activeImage.size_bytes)} • {formatDate(activeImage.created_at)}
                </p>
              </div>
              <div className="modal-actions">
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={(e) => handleDownload(activeImage, e)}
                >
                  ↓ Download
                </button>
                <button
                  type="button"
                  className="btn btn-ghost"
                  onClick={(e) => handleCopyLink(activeImage, e)}
                >
                  {copiedFilename === activeImage.filename ? "✓ Copied" : "🔗 Copy Link"}
                </button>
                {onUseAsReference && (
                  <button
                    type="button"
                    className="btn btn-ghost"
                    onClick={(e) => handleUseAsRef(activeImage, e)}
                  >
                    📌 Use as Reference
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
} 
