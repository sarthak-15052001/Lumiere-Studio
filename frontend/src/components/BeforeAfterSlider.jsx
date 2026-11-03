import { useState, useRef, useEffect } from "react";

export default function BeforeAfterSlider({ beforeImage, afterImage, title, description }) {
  const [sliderPosition, setSliderPosition] = useState(50);
  const containerRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleMouseDown = () => setIsDragging(true);
  const handleMouseUp = () => setIsDragging(false);
  const handleMouseLeave = () => setIsDragging(false);

  const handleMouseMove = (e) => {
    if (!isDragging || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
    setSliderPosition(percentage);
  };

  const handleTouchStart = () => setIsDragging(true);
  const handleTouchEnd = () => setIsDragging(false);
  const handleTouchMove = (e) => {
    if (!isDragging || !containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = e.touches[0].clientX - rect.left;
    const percentage = Math.max(0, Math.min(100, (x / rect.width) * 100));
    setSliderPosition(percentage);
  };

  useEffect(() => {
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
    window.addEventListener("touchmove", handleTouchMove);
    window.addEventListener("touchend", handleTouchEnd);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
      window.removeEventListener("touchmove", handleTouchMove);
      window.removeEventListener("touchend", handleTouchEnd);
    };
  }, [isDragging]);

  return (
    <div className="before-after-container">
      {title && <h3 className="before-after-title">{title}</h3>}
      {description && <p className="before-after-desc">{description}</p>}
      
      <div
        className="before-after-slider"
        ref={containerRef}
        onMouseDown={handleMouseDown}
        onTouchStart={handleTouchStart}
      >
        {/* After image (background) */}
        <div className="before-after-after">
          {typeof afterImage === "string" ? (
            <img src={afterImage} alt="After" />
          ) : (
            afterImage
          )}
          <span className="before-after-label">After</span>
        </div>

        {/* Before image (overlay) */}
        <div
          className="before-after-before"
          style={{ width: `${sliderPosition}%` }}
        >
          {typeof beforeImage === "string" ? (
            <img src={beforeImage} alt="Before" />
          ) : (
            beforeImage
          )}
          <span className="before-after-label">Before</span>
        </div>

        {/* Slider handle */}
        <div
          className={`before-after-handle ${isDragging ? "is-dragging" : ""}`}
          style={{ left: `${sliderPosition}%` }}
        >
          <div className="before-after-handle-bar" />
          <div className="before-after-handle-arrow before-after-handle-arrow-left">‹</div>
          <div className="before-after-handle-arrow before-after-handle-arrow-right">›</div>
        </div>
      </div>
    </div>
  );
}