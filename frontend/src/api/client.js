// import axios from "axios";


// export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// export const api = axios.create({
//   baseURL: API_BASE_URL,
//   timeout: 5 * 60 * 1000, // generation can take a while (polling job queues server-side)
// });


// export function resolveAssetUrl(downloadUrl) {
//   if (!downloadUrl) return null;

//   try {
//     const path = new URL(downloadUrl).pathname; // e.g. "/static/abc123.png"
//     if (API_BASE_URL.startsWith("http")) {
//       const origin = new URL(API_BASE_URL).origin;
//       return `${origin}${path}`;
//     }
//     // API_BASE_URL is a relative path like "/api" (dev proxy mode) ->
//     // static files are proxied separately, see vite.config.js
//     return path;
//   } catch {
//     return downloadUrl;
//   }
// }

// /**
//  * POST /generate — single product image, optional AI model on it.
//  * formValues matches the FastAPI Form(...) fields in app/route.py exactly.
//  */
// export async function generateImage(formValues, file) {
//   const form = new FormData();
//   form.append("file", file);
//   form.append("product_name", formValues.productName);
//   form.append("brand_name", formValues.brandName || "");
//   form.append("studio_type", formValues.studioType);
//   form.append("category", formValues.category);
//   form.append("target_audience", formValues.targetAudience || "");
//   form.append("region", formValues.region || "None");
//   form.append("apparel_style", formValues.apparelStyle || "Professional");
//   form.append("style_preset", formValues.stylePreset || "Modern");
//   form.append("background", formValues.background || "Solid White");
//   form.append("num_images", String(formValues.numImages || 1));
//   if (formValues.background === "Custom Idea" && formValues.customBackground) {
//     form.append("custom_background", formValues.customBackground);
//   }
//   form.append("additional_instructions", formValues.additionalInstructions || "");

//   const { data } = await api.post("/generate", form, {
//     headers: { "Content-Type": "multipart/form-data" },
//   });
//   return data;
// }

// /**
//  * POST /generate-dual — Custom Model Studio: an uploaded reference model
//  * (own_image) plus a separate product image (product_image). No "region"
//  * field on this endpoint (see app/route.py generate_dual signature).
//  */
// export async function generateDualImage(formValues, ownImageFile, productImageFile) {
//   const form = new FormData();
//   form.append("own_image", ownImageFile);
//   form.append("product_image", productImageFile);
//   form.append("product_name", formValues.productName);
//   form.append("brand_name", formValues.brandName || "");
//   form.append("studio_type", formValues.studioType);
//   form.append("category", formValues.category);
//   form.append("target_audience", formValues.targetAudience || "");
//   form.append("apparel_style", formValues.apparelStyle || "Professional");
//   form.append("style_preset", formValues.stylePreset || "Modern");
//   form.append("background", formValues.background || "Solid White");
//   form.append("num_images", String(formValues.numImages || 1));
//   if (formValues.background === "Custom Idea" && formValues.customBackground) {
//     form.append("custom_background", formValues.customBackground);
//   }
//   form.append("additional_instructions", formValues.additionalInstructions || "");

//   const { data } = await api.post("/generate-dual", form, {
//     headers: { "Content-Type": "multipart/form-data" },
//   });
//   return data;
// }

// /**
//  * GET /gallery — every image currently sitting in the backend's static/
//  * folder (i.e. everything ever generated), newest first.
//  * Each item is normalized to { filename, url, size_bytes, created_at }.
//  */
// export async function getGallery() {
//   const { data } = await api.get("/gallery");
//   const images = Array.isArray(data?.images) ? data.images : [];
//   return images.map((item) => ({
//     ...item,
//     url: resolveAssetUrl(item.url),
//   }));
// }

import axios from "axios";


export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5 * 60 * 1000, // generation can take a while (polling job queues server-side)
});


export function resolveAssetUrl(downloadUrl) {
  if (!downloadUrl) return null;

  try {
    const path = new URL(downloadUrl).pathname; // e.g. "/static/abc123.png"
    if (API_BASE_URL.startsWith("http")) {
      const origin = new URL(API_BASE_URL).origin;
      return `${origin}${path}`;
    }
    // API_BASE_URL is a relative path like "/api" (dev proxy mode) ->
    // static files are proxied separately, see vite.config.js
    return path;
  } catch {
    return downloadUrl;
  }
}

/**
 * POST /generate — single product image, optional AI model on it.
 * formValues matches the FastAPI Form(...) fields in app/route.py exactly.
 */
export async function generateImage(formValues, file) {
  const form = new FormData();
  form.append("file", file);
  form.append("product_name", formValues.productName);
  form.append("brand_name", formValues.brandName || "");
  form.append("studio_type", formValues.studioType);
  form.append("category", formValues.category);
  form.append("target_audience", formValues.targetAudience || "");
  form.append("region", formValues.region || "None");
  form.append("apparel_style", formValues.apparelStyle || "Professional");
  form.append("style_preset", formValues.stylePreset || "Modern");
  form.append("background", formValues.background || "Solid White");
  form.append("num_images", String(formValues.numImages || 1));
  if (formValues.background === "Custom Idea" && formValues.customBackground) {
    form.append("custom_background", formValues.customBackground);
  }
  form.append("additional_instructions", formValues.additionalInstructions || "");

  const { data } = await api.post("/generate", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

/**
 * POST /generate-dual — Custom Model Studio: an uploaded reference model
 * (own_image) plus a separate product image (product_image). No "region"
 * field on this endpoint (see app/route.py generate_dual signature).
 */
export async function generateDualImage(formValues, ownImageFile, productImageFile) {
  const form = new FormData();
  form.append("own_image", ownImageFile);
  form.append("product_image", productImageFile);
  form.append("product_name", formValues.productName);
  form.append("brand_name", formValues.brandName || "");
  form.append("studio_type", formValues.studioType);
  form.append("category", formValues.category);
  form.append("target_audience", formValues.targetAudience || "");
  form.append("apparel_style", formValues.apparelStyle || "Professional");
  form.append("style_preset", formValues.stylePreset || "Modern");
  form.append("background", formValues.background || "Solid White");
  form.append("num_images", String(formValues.numImages || 1));
  if (formValues.background === "Custom Idea" && formValues.customBackground) {
    form.append("custom_background", formValues.customBackground);
  }
  form.append("additional_instructions", formValues.additionalInstructions || "");

  const { data } = await api.post("/generate-dual", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

/**
 * GET /gallery — every image currently sitting in the backend's static/
 * folder (i.e. everything ever generated), newest first.
 * Each item is normalized to:
 *   { filename, url, size_bytes, created_at, product_name, brand_name, category, studio_type }
 */
export async function getGallery() {
  const { data } = await api.get("/gallery");
  const images = Array.isArray(data?.images) ? data.images : [];
  return images.map((item) => ({
    ...item,
    url: resolveAssetUrl(item.url),
  }));
}