# import os
# from fastapi import APIRouter, File, Form, HTTPException, UploadFile
# import requests
# from fastapi import Request
# from app.dual_img import build_dual_prompt, generate_dual_image
# from app.service import build_prompt, generate_image
# from app.dual_img import get_apiframe_job
# from fastapi import Query
# from .service import get_apiframe_job


# router     = APIRouter()
# STATIC_DIR = "static"
# os.makedirs(STATIC_DIR, exist_ok=True)

# IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")


# @router.get("/gallery")
# def list_gallery(request: Request):
#     """Return every generated image sitting in the static/ folder, newest first."""
#     base_url = str(request.base_url).rstrip("/")

#     items = []
#     for filename in os.listdir(STATIC_DIR):
#         if not filename.lower().endswith(IMAGE_EXTENSIONS):
#             continue
#         filepath = os.path.join(STATIC_DIR, filename)
#         if not os.path.isfile(filepath):
#             continue
#         stat = os.stat(filepath)
#         items.append({
#             "filename": filename,
#             "url": f"{base_url}/static/{filename}",
#             "size_bytes": stat.st_size,
#             "created_at": stat.st_mtime,
#         })

#     items.sort(key=lambda item: item["created_at"], reverse=True)
#     return {"count": len(items), "images": items}


# @router.post("/apiframe/webhook")
# async def apiframe_webhook(request: Request):
#     try:
#         payload = await request.json()
#     except Exception:
#         body = await request.body()
#         print("Raw webhook body:", body)
#         return {"message": "Invalid JSON"}

#     print("Webhook Received:", payload)

#     status = payload.get("status")
#     if status != "COMPLETED":
#         return {"message": "Waiting"}

#     images = payload.get("images", [])
#     if not images:
#         return {"message": "No Images"}

#     for image_url in images:
#         filename = image_url.split("/")[-1]
#         filepath = os.path.join(STATIC_DIR, filename)
#         response = requests.get(image_url)
#         if response.status_code == 200:
#             with open(filepath, "wb") as f:
#                 f.write(response.content)
#             print("Saved:", filepath)

#     return {"message": "Done"}


# @router.post("/generate")
# async def generate(
#     file: UploadFile = File(...),
#     product_name: str = Form(...),
#     brand_name: str = Form(""),
#     studio_type: str = Form(...),
#     category: str = Form(...),
#     target_audience: str = Form(""),
#     region: str = Form("Indian"),
#     apparel_style: str = Form("Professional"),
#     style_preset: str = Form("Modern"),
#     background: str = Form("Solid White"),
#     num_images: int = Form(1),
#     custom_background: str = Form(None),
#     additional_instructions: str = Form(""),
# ):
#     region = region.strip() or "None"

#     prompts, negative_prompt = build_prompt(
#         studio_type=studio_type, category=category,
#         target_audience=target_audience, product_name=product_name,
#         brand_name=brand_name, background=background,
#         style_preset=style_preset, apparel_style=apparel_style,
#         num_images=num_images, model_region=region,
#         custom_background=custom_background,
#         additional_instructions=additional_instructions or "",
#     )
#     print("📦 Uploaded file:", file.filename)
#     print(f"\n{'='*60}\n📸 PROMPT: {prompts[0][:3000]}\n{'='*60}")

#     result = await generate_image(prompts[0], negative_prompt, file)
#     if result.get("status") == "error":
#         raise HTTPException(status_code=503, detail=result["message"])

#     filename = result["filename"]
#     print(f"🖼️  Saved: static/{filename}")

#     return {
#         "status":       "completed",
#         "download_url": f"http://localhost:8000/static/{filename}",
#     }


# @router.post("/generate-dual")
# async def generate_dual(
#     own_image: UploadFile = File(...),
#     product_image: UploadFile = File(...),
#     product_name: str = Form(...),
#     brand_name: str = Form(""),
#     studio_type: str = Form(...),
#     category: str = Form(...),
#     target_audience: str = Form(""),
#     apparel_style: str = Form("Professional"),
#     style_preset: str = Form("Modern"),
#     background: str = Form("Solid White"),
#     num_images: int = Form(1),
#     custom_background: str = Form(None),
#     additional_instructions: str = Form(""),
# ):
#     prompts, negative_prompt = build_dual_prompt(
#         studio_type=studio_type,
#         category=category,
#         target_audience=target_audience,
#         product_name=product_name,
#         brand_name=brand_name,
#         background=background,
#         style_preset=style_preset,
#         apparel_style=apparel_style,
#         num_images=num_images,
#         custom_background=custom_background,
#         additional_instructions=additional_instructions or "",
#     )
#     print("📦 Uploaded file:", own_image.filename)
#     print("📦 Uploaded file 2:", product_image.filename)
#     print(f"\n{'='*60}\n📸 PROMPT: {prompts[0][:3000]}\n{'='*60}")
    
#     result = await generate_dual_image(prompts[0], negative_prompt, own_image, product_image)
#     if result.get("status") == "error":
#         raise HTTPException(status_code=503, detail=result["message"])

#     filename = result["filename"]
#     print(f"🖼️  Saved: static/{filename}")
#     return {
#         "status": "completed",
#         "download_url": f"http://localhost:8000/static/{filename}",
#     }



# @router.get("/apiframe/job")
# def apiframe_job_status(
#     job_id: str = Query(..., description="APIFrame Job ID"),
#     api_key: str = Query(..., description="APIFrame API Key")
# ):

#     return get_apiframe_job(job_id, api_key)

# # @router.get("/apiframe/job")
# # def apiframe_job(
# #     job_id: str = Query(...),
# #     api_key: str = Query(...)
# # ):
# #     return get_apiframe_job(job_id, api_key)

import os
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
import requests
from fastapi import Request
from app.dual_img import build_dual_prompt, generate_dual_image
from app.service import build_prompt, generate_image
from app.dual_img import get_apiframe_job
from fastapi import Query
from .service import get_apiframe_job
from app.gallery_meta import load_metadata


router     = APIRouter()
STATIC_DIR = "static"
os.makedirs(STATIC_DIR, exist_ok=True)

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")


@router.get("/gallery")
def list_gallery(request: Request):
    """Every generated image in static/, newest first.

    Each item carries product_name / brand_name / category when available
    (recorded at generation time), so the frontend can show and search by the
    real product name instead of guessing one from the filename.
    """
    base_url = str(request.base_url).rstrip("/")
    metadata = load_metadata()

    items = []
    for filename in os.listdir(STATIC_DIR):
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue
        filepath = os.path.join(STATIC_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        stat = os.stat(filepath)
        meta = metadata.get(filename, {})
        items.append({
            "filename": filename,
            "url": f"{base_url}/static/{filename}",
            "size_bytes": stat.st_size,
            "created_at": stat.st_mtime,
            "product_name": meta.get("product_name"),
            "brand_name": meta.get("brand_name"),
            "category": meta.get("category"),
            "studio_type": meta.get("studio_type"),
        })

    items.sort(key=lambda item: item["created_at"], reverse=True)
    return {"count": len(items), "images": items}

@router.post("/apiframe/webhook")
async def apiframe_webhook(request: Request):
    try:
        payload = await request.json()
    except Exception:
        body = await request.body()
        print("Raw webhook body:", body)
        return {"message": "Invalid JSON"}

    print("Webhook Received:", payload)

    status = payload.get("status")
    if status != "COMPLETED":
        return {"message": "Waiting"}

    images = payload.get("images", [])
    if not images:
        return {"message": "No Images"}

    for image_url in images:
        filename = image_url.split("/")[-1]
        filepath = os.path.join(STATIC_DIR, filename)
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            print("Saved:", filepath)

    return {"message": "Done"}


@router.post("/generate")
async def generate(
    file: UploadFile = File(...),
    product_name: str = Form(...),
    brand_name: str = Form(""),
    studio_type: str = Form(...),
    category: str = Form(...),
    target_audience: str = Form(""),
    region: str = Form("Indian"),
    apparel_style: str = Form("Professional"),
    style_preset: str = Form("Modern"),
    background: str = Form("Solid White"),
    num_images: int = Form(1),
    custom_background: str = Form(None),
    additional_instructions: str = Form(""),
):
    region = region.strip() or "None"

    prompts, negative_prompt = build_prompt(
        studio_type=studio_type, category=category,
        target_audience=target_audience, product_name=product_name,
        brand_name=brand_name, background=background,
        style_preset=style_preset, apparel_style=apparel_style,
        num_images=num_images, model_region=region,
        custom_background=custom_background,
        additional_instructions=additional_instructions or "",
    )
    print("📦 Uploaded file:", file.filename)
    print(f"\n{'='*60}\n📸 PROMPT: {prompts[0][:3000]}\n{'='*60}")

    result = await generate_image(
        prompts[0],
        negative_prompt,
        file,
        product_name=product_name,
        brand_name=brand_name,
        category=category,
        studio_type=studio_type,
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=503, detail=result["message"])

    filename = result["filename"]
    print(f"🖼️  Saved: static/{filename}")

    return {
        "status":       "completed",
        "download_url": f"http://localhost:8000/static/{filename}",
    }


@router.post("/generate-dual")
async def generate_dual(
    own_image: UploadFile = File(...),
    product_image: UploadFile = File(...),
    product_name: str = Form(...),
    brand_name: str = Form(""),
    studio_type: str = Form(...),
    category: str = Form(...),
    target_audience: str = Form(""),
    apparel_style: str = Form("Professional"),
    style_preset: str = Form("Modern"),
    background: str = Form("Solid White"),
    num_images: int = Form(1),
    custom_background: str = Form(None),
    additional_instructions: str = Form(""),
):
    prompts, negative_prompt = build_dual_prompt(
        studio_type=studio_type,
        category=category,
        target_audience=target_audience,
        product_name=product_name,
        brand_name=brand_name,
        background=background,
        style_preset=style_preset,
        apparel_style=apparel_style,
        num_images=num_images,
        custom_background=custom_background,
        additional_instructions=additional_instructions or "",
    )
    print("📦 Uploaded file:", own_image.filename)
    print("📦 Uploaded file 2:", product_image.filename)
    print(f"\n{'='*60}\n📸 PROMPT: {prompts[0][:3000]}\n{'='*60}")
    
    result = await generate_dual_image(
        prompts[0],
        negative_prompt,
        own_image,
        product_image,
        product_name=product_name,
        brand_name=brand_name,
        category=category,
        studio_type=studio_type,
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=503, detail=result["message"])

    filename = result["filename"]
    print(f"🖼️  Saved: static/{filename}")
    return {
        "status": "completed",
        "download_url": f"http://localhost:8000/static/{filename}",
    }



@router.get("/apiframe/job")
def apiframe_job_status(
    job_id: str = Query(..., description="APIFrame Job ID"),
    api_key: str = Query(..., description="APIFrame API Key")
):

    return get_apiframe_job(job_id, api_key)

# @router.get("/apiframe/job")
# def apiframe_job(
#     job_id: str = Query(...),
#     api_key: str = Query(...)
# ):
#     return get_apiframe_job(job_id, api_key)