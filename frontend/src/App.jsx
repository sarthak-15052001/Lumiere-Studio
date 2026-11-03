import React, { useState } from "react";
import CreateStudio from "./components/CreateStudio.jsx";
import Gallery from "./components/Gallery.jsx";
import BeforeAfterSlider from "./components/BeforeAfterSlider.jsx";
import ProcessGuide from "./components/ProcessGuide.jsx";
import beforeImage from "./asset/before.jpeg";
import afterImage from "./asset/after.png";
import headphoneBefore from "./asset/headphone-Before.jpeg";
import headphoneAfter from "./asset/headphone-after.png";
import watchBefore from "./asset/watch-before.png";
import watchAfter from "./asset/watch-after.png";
import "./App.css";

function SparkleMark({ className = "" }) {
  return (
    <svg className={className} viewBox="0 0 48 48" role="img" aria-label="Lumière sparkle">
      <path d="M24 2.5c2.9 11.4 8.1 16.6 21.5 21.5C32.1 28.9 26.9 34.1 24 45.5 21.1 34.1 15.9 28.9 2.5 24 15.9 19.1 21.1 13.9 24 2.5Z" fill="currentColor" />
      <path d="M39 2c1.1 4.1 2.9 5.9 7 7-4.1 1.1-5.9 2.9-7 7-1.1-4.1-2.9-5.9-7-7 4.1-1.1 5.9-2.9 7-7Z" fill="currentColor" opacity=".65" />
    </svg>
  );
}

const FEATURES = [
  {
    icon: "🎨",
    title: "AI-Powered Styling",
    desc: "Generative AI creates professional product shots with cinematic lighting, perfect backgrounds, and studio-quality results in seconds.",
  },
  {
    icon: "👗",
    title: "Fashion & Apparel",
    desc: "Dress your products on AI-generated models across Indian, Western, and global aesthetics — no physical photoshoot needed.",
  },
  {
    icon: "⚡",
    title: "Instant Results",
    desc: "Upload your product image, pick a style, and get professional-grade visuals in under 60 seconds. No design skills required.",
  },
  {
    icon: "🖼️",
    title: "Custom Model Studio",
    desc: "Upload your own model reference photo and let AI seamlessly blend your product onto it with natural lighting and pose.",
  },
  {
    icon: "🌍",
    title: "Multi-Region Models",
    desc: "Generate images featuring Indian, Western, East Asian, and Middle Eastern models to reach your target audience globally.",
  },
  {
    icon: "📦",
    title: "E-commerce Ready",
    desc: "Get clean catalog shots, lifestyle images, and marketing visuals — all optimized for Amazon, Flipkart, Shopify, and more.",
  },
];

const HOW_IT_WORKS = [
  {
    step: "01",
    title: "Choose Your Studio",
    desc: "Select Photo Studio, Marketing Studio, or Custom Model Studio based on your product and campaign goals.",
  },
  {
    step: "02",
    title: "Upload Your Product",
    desc: "Drop in a clear photo of your product. Our AI analyzes it and prepares it for professional styling.",
  },
  {
    step: "03",
    title: "Customize the Look",
    desc: "Pick backgrounds, style presets, model regions, and apparel styles to match your brand identity.",
  },
  {
    step: "04",
    title: "Generate & Download",
    desc: "Hit generate and watch AI create stunning visuals. Download instantly or save to your gallery.",
  },
];

const STUDIO_PREVIEW_OPTIONS = [
  {
    title: "Photo Studio",
    icon: "📷",
    badge: "Catalog",
    desc: "Clean, high-conversion images with plain product backdrops and crisp detail.",
    points: ["E-commerce ready", "Crisp product focus", "Fast generation"],
  },
  {
    title: "Marketing Studio",
    icon: "🎬",
    badge: "Campaign",
    desc: "Lifestyle-style compositions that help your product feel premium and aspirational.",
    points: ["Lifestyle scenes", "Cinematic lighting", "Brand storytelling"],
  },
  {
    title: "Custom Model Studio",
    icon: "👗",
    badge: "Personalized",
    desc: "Blend your product onto your own model reference with accurate styling and pose.",
    points: ["Your model photo", "Natural fit", "Best for fashion"],
  },
];

const BLOG_POSTS = [
  {
    tag: "Before / After",
    title: "Product to Campaign: Headphones",
    desc: "See a studio-style before/after transformation with precision lighting and premium placement.",
    beforeImage: headphoneBefore,
    afterImage: headphoneAfter,
  },
  {
    tag: "Before / After",
    title: "Modern Watch, Modern Look",
    desc: "From raw product shot to polished campaign visual with crisp reflection and depth.",
    beforeImage: watchBefore,
    afterImage: watchAfter,
  },
  {
    tag: "Before / After",
    title: "Minimal Product → Branded Lifestyle",
    desc: "Quickly turn plain product imagery into store-ready marketing visuals that sell.",
    beforeImage: beforeImage,
    afterImage: afterImage,
  },
];

function HomePage({ onGetStarted, onOpenGallery, onOpenHowItWorks }) {
  return (
    <div id="home" className="home">
      {/* Hero */}
      <section className="hero">
        <div className="hero-glow hero-glow-1" />
        <div className="hero-glow hero-glow-2" />
        <div className="hero-content">
          <div className="hero-badge">
            <span className="hero-badge-dot" />
            Powered by Generative AI · Built for product visuals
          </div>
          <h1 className="hero-title">
            Studio-grade product visuals
            <span className="hero-title-accent"> in one smooth workflow</span>
          </h1>
          <p className="hero-sub">
            Upload your product, choose a premium style, and generate polished catalog or lifestyle images with AI-first speed.
          </p>
          <div className="hero-actions">
            <button className="btn btn-primary btn-lg" onClick={onGetStarted}>
              Create Studio →
            </button>
            <button className="btn btn-ghost btn-lg" onClick={onOpenGallery}>
              Explore Gallery
            </button>
          </div>
          <div className="hero-stats">
            <div className="hero-stat">
              <span className="hero-stat-num">500+</span>
              <span className="hero-stat-label">SKUs Generated</span>
            </div>
            <div className="hero-stat">
              <span className="hero-stat-num">60s</span>
              <span className="hero-stat-label">Per Image</span>
            </div>
            <div className="hero-stat">
              <span className="hero-stat-num">80%</span>
              <span className="hero-stat-label">Cost Reduction</span>
            </div>
          </div>
        </div>
        <div className="hero-visual">
          <div className="hero-preview-card">
            <div className="hero-preview-frame">
              <div className="hero-preview-side hero-preview-side-before">
                <span className="hero-preview-label">Before</span>
                <div className="hero-preview-emoji">🛍️</div>
              </div>
              <div className="hero-preview-side hero-preview-side-after">
                <span className="hero-preview-label">After</span>
                <div className="hero-preview-emoji">👗</div>
              </div>
            </div>
            <div className="hero-preview-footer">
              <span>Before / after look</span>
              <span>Studio ready</span>
            </div>
          </div>
        </div>
      </section>

      <section className="section studio-showcase">
        <div className="section-inner">
          <div className="section-head">
            <span className="section-eyebrow">Create Studio</span>
            <h2 className="section-title">Choose the right studio for your product</h2>
            <p className="section-sub">
              Each option is designed for a different use case — catalog shots, campaign visuals, or tailored model-based imagery.
            </p>
          </div>
          <div className="studio-card-grid">
            {STUDIO_PREVIEW_OPTIONS.map((item) => (
              <div className="studio-preview-card" key={item.title}>
                <div className="studio-card-top">
                  <span className="studio-card-icon">{item.icon}</span>
                  <span className="studio-card-badge">{item.badge}</span>
                </div>
                <h3 className="studio-card-title">{item.title}</h3>
                <p className="studio-card-desc">{item.desc}</p>
                <ul className="studio-card-points">
                  {item.points.map((point) => (
                    <li key={point}>{point}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <div className="section-cta">
            <button className="btn btn-primary btn-lg" onClick={onGetStarted}>
              Start Creating Now →
            </button>
            <button className="btn btn-ghost btn-lg" onClick={onOpenHowItWorks}>
              See How It Works
            </button>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="section">
        <div className="section-inner">
          <div className="section-head">
            <span className="section-eyebrow">What We Do</span>
            <h2 className="section-title">Everything you need for product visuals</h2>
            <p className="section-sub">
              Lumière Studio is a generative AI platform for e-commerce and fashion brands.
            </p>
          </div>
          <div className="features-grid">
            {FEATURES.map((f) => (
              <div className="feature-card" key={f.title}>
                <div className="feature-icon">{f.icon}</div>
                <h3 className="feature-title">{f.title}</h3>
                <p className="feature-desc">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works - Interactive */}
      <section id="how-it-works" className="section section-alt">
        <div className="section-inner">
          <div className="section-head">
            <span className="section-eyebrow">How It Works</span>
            <h2 className="section-title">4 Simple Steps to Professional Visuals</h2>
            <p className="section-sub">
              Interactive walkthrough — follow along and see how easy it is to create stunning product images.
            </p>
          </div>
          <ProcessGuide />
          <div className="section-cta">
            <button className="btn btn-primary btn-lg" onClick={onGetStarted}>
              Start Your First Generation →
            </button>
          </div>
        </div>
      </section>

      {/* Blog / Before-After Showcase */}
      <section className="section">
        <div className="section-inner">
          <div className="section-head">
            <span className="section-eyebrow">Blog & Case Studies</span>
            <h2 className="section-title">See the Transformation</h2>
            <p className="section-sub">
              Drag the slider to see before/after examples and explore product visual styles.
            </p>
          </div>
          <div className="blog-showcase-grid">
            {BLOG_POSTS.map((post, idx) => (
              <div className="blog-showcase-card" key={post.title}>
                <div className="blog-showcase-slider">
                  <BeforeAfterSlider
                    beforeImage={post.beforeImage}
                    afterImage={post.afterImage}
                    title={post.title}
                    description={post.desc}
                  />
                </div>
                <div className="blog-showcase-footer">
                  <span className="blog-tag">{post.tag}</span>
                  <button className="btn btn-ghost blog-read-btn" onClick={onGetStarted}>
                    Learn More →
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Banner */}
      <section className="cta-banner">
        <div className="cta-banner-glow" />
        <div className="cta-banner-inner">
          <h2 className="cta-banner-title">Ready to transform your product photos?</h2>
          <p className="cta-banner-sub">
            Create polished product visuals for your brand at scale.
          </p>
          <button className="btn btn-primary btn-lg" onClick={onGetStarted}>
            Launch Studio →
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-inner">
          <div className="footer-brand">
            <SparkleMark className="footer-brand-mark" />
            <span className="footer-brand-name">LUMIÈRE STUDIO</span>
          </div>
          <p className="footer-copy">
            © {new Date().getFullYear()} Lumière Studio · All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default function App() {
  const [view, setView] = useState("home"); // home | studio | gallery
  const [refImage, setRefImage] = useState(null);

  const goToStudio = () => setView("studio");

  const handleHowItWorks = () => {
    if (view !== "home") {
      setView("home");
      setTimeout(() => {
        document.getElementById("how-it-works")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 80);
      return;
    }
    document.getElementById("how-it-works")?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const handleUseAsReference = async (img) => {
    try {
      const allowedOrigins = [window.location.origin, new URL(import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").origin];
      const imgOrigin = new URL(img.url).origin;
      if (!allowedOrigins.includes(imgOrigin)) throw new Error("Untrusted image origin");
      setRefImage(img);
      setView("studio");
    } catch (err) {
      console.error("Couldn't use this image as a reference:", err);
    }
  };

  return (
    <div className="shell">
      <header className="topbar">
        <button className="brandmark" onClick={() => setView("home")} type="button">
          <SparkleMark className="brandmark-mark" />
          <span className="brandmark-name">LUMIÈRE STUDIO</span>
        </button>

        <nav className="topnav" aria-label="View">
          <button
            type="button"
            className={`topnav-btn ${view === "home" ? "is-active" : ""}`}
            onClick={() => setView("home")}
          >
            Home
          </button>
          <button
            type="button"
            className={`topnav-btn ${view === "studio" ? "is-active" : ""}`}
            onClick={goToStudio}
          >
            Create Studio
          </button>
          <button
            type="button"
            className={`topnav-btn ${view === "gallery" ? "is-active" : ""}`}
            onClick={() => setView("gallery")}
          >
            Gallery
          </button>
          <button
            type="button"
            className={`topnav-btn ${view === "home" ? "is-active" : ""}`}
            onClick={handleHowItWorks}
          >
            How It Works
          </button>
        </nav>
      </header>

      {view === "home" && (
        <HomePage
          onGetStarted={goToStudio}
          onOpenGallery={() => setView("gallery")}
          onOpenHowItWorks={handleHowItWorks}
        />
      )}

      {view === "gallery" && (
        <div className="layout-full">
          <main className="stage stage-wide">
            <Gallery onUseAsReference={handleUseAsReference} />
          </main>
        </div>
      )}

      {view === "studio" && (
        <div className="cs-page">
          <main className="cs-stage">
            <CreateStudio
              onStartOver={() => setView("home")}
              onViewGallery={() => setView("gallery")}
            />
          </main>
        </div>
      )}
    </div>
  );
}
