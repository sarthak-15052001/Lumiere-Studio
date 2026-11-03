# import base64
# import os
# import time
# import uuid
# from io import BytesIO
# import requests
# from PIL import Image
# from app.config import APIFRAME_API_KEY, IMGBB_API_KEY

# PROMPT_LIMIT = 4000  # safe limit for Flux 2 Pro
# STATIC_DIR = "static"


# async def image_to_pil(file):
#     content = await file.read()
#     return Image.open(BytesIO(content)).convert("RGB")


# def save_image(pil_image):
#     os.makedirs(STATIC_DIR, exist_ok=True)
#     filename = f"{uuid.uuid4().hex}.png"
#     path = os.path.join(STATIC_DIR, filename)
#     pil_image.save(path, "PNG")
#     return filename


# def upload_image_to_imgbb(input_image: Image.Image) -> str:
     
#     buffered = BytesIO()
#     input_image.save(buffered, format="PNG")
#     base64_image = base64.b64encode(buffered.getvalue()).decode()

#     resp = requests.post(
#         "https://api.imgbb.com/1/upload",
#         data={"key": IMGBB_API_KEY, "image": base64_image},
#         timeout=60,
#     )
#     if resp.status_code != 200:
         
#         raise Exception(f"imgbb upload failed: {resp.text}")

#     url = resp.json().get("data", {}).get("url")
#     if not url:
#         raise Exception(f"No URL from imgbb: {resp.json()}")
#     return url


# MAX_POLLS = 100

# def apiframe_dual_image_to_image(prompt: str, input_image: Image.Image, input_image_2: Image.Image):
#     image_url_1 = upload_image_to_imgbb(input_image)
#     image_url_2 = upload_image_to_imgbb(input_image_2)

#     response = requests.post(
#         "https://api.apiframe.ai/v2/images/generate",
#         headers={"X-API-Key": APIFRAME_API_KEY, "Content-Type": "application/json"},
#         json={
#             "prompt": prompt,
#             "model": "nano-banana",
#             "nanoBananaParams": {"image_input": [image_url_1, image_url_2], "output_format": "png"}
#         },
#         timeout=120
#     )
#     response.raise_for_status()
#     job_id = response.json().get("jobId")
#     if not job_id:
#         raise Exception(f"No jobId returned: {response.json()}")
#     print(f"Job ID: {job_id}")

#     for attempt in range(MAX_POLLS):
#         # ✅ correct endpoint
#         poll = requests.get(
#             f"https://api.apiframe.ai/v2/jobs/{job_id}",
#             headers={"X-API-Key": APIFRAME_API_KEY},
#             timeout=30
#         )
#         poll.raise_for_status()
#         data = poll.json()
#         status = data.get("status")
#         print(f"[{attempt+1}/{MAX_POLLS}] Status: {status} ({data.get('progress')}%)")

#         if status in ("QUEUED", "PROCESSING"):
#             time.sleep(3)
#         elif status == "FAILED":
#             raise Exception(f"Generation failed: {data.get('error')}")
#         elif status == "COMPLETED":
#             # ✅ correct parsing
#             images = (data.get("result") or {}).get("images")
#             if not images:
#                 raise Exception(f"No images returned: {data}")
#             img_resp = requests.get(images[0], timeout=60)
#             img_resp.raise_for_status()
#             return Image.open(BytesIO(img_resp.content)).convert("RGB")
#         else:
#             print(f"Unknown status '{status}', retrying...")
#             time.sleep(3)

#     raise Exception(f"Job timed out after {MAX_POLLS * 3}s")

# def get_apiframe_job(job_id: str, api_key: str):

#     response = requests.get(
#         f"https://api.apiframe.ai/v2/jobs/{job_id}",
#         headers={
#             "X-API-Key": api_key
#         },
#         timeout=300
#     )

#     response.raise_for_status()

#     data = response.json()

#     # Job still running
#     if data.get("status") != "COMPLETED":
#         return data

#     # Download image
#     image_url = data["result"]["images"][0]

#     img_resp = requests.get(image_url, timeout=60)
#     img_resp.raise_for_status()

#     image = Image.open(BytesIO(img_resp.content)).convert("RGB")

#     filename = save_image(image)

#     return {
#         "status": data["status"],
#         "job_id": job_id,
#         "image_url": image_url,
#         "filename": filename,
#         "download_url": f"/static/{filename}"
#     }

# import asyncio

# async def generate_dual_image(prompt: str, negative_prompt: str, file, file_2):
#     try:
#         input_image = await image_to_pil(file)
#         input_image_2 = await image_to_pil(file_2)
#         loop = asyncio.get_event_loop()
#         image = await loop.run_in_executor(
#             None, apiframe_dual_image_to_image, prompt, input_image, input_image_2
#         )
#         filename = save_image(image)
#         return {"status": "success", "filename": filename, "provider": "apiframe"}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}



# def truncate_prompt(text: str, max_chars: int = PROMPT_LIMIT) -> str:
#     if len(text) <= max_chars:
#         return text
#     truncated = text[:max_chars].rsplit(' ', 1)[0].rstrip(', ')
#     print(f"⚠️  PROMPT TRUNCATED: {len(text)} → {len(truncated)} chars (limit={max_chars})")
#     return truncated




 
# def build_dual_prompt(
#     studio_type,
#     category,
#     target_audience,
#     product_name,
#     brand_name,
#     background,
#     style_preset,
#     apparel_style=None,
#     num_images=1,
#     custom_background=None,
#     additional_instructions=""
# ):
#     """
#     Dual-image Product-on-Person prompt builder.
#     Image 1 (input_image)   = user's own photo — person is the base.
#     Image 2 (input_image_2) = product photo   — AI detects type and places it.
#     Supports 1-4 stylistic variations.
#     """

#     if num_images < 1 or num_images > 4:
#         raise ValueError("num_images must be between 1 and 4")

#     # Sanitise free text
#     product_name            = product_name.strip()[:80]
#     brand_name              = brand_name.strip()[:40]
#     additional_instructions = additional_instructions.strip()[:150]
#     if custom_background:
#         custom_background = custom_background.strip()[:100]

#     # Background
#     print(f"DEBUG dual: background='{background}'")
#     background = background.strip()
#     if background == "Solid White":
#         background_details = "clean white seamless backdrop, shadow under feet, studio floor visible"
#     elif background == "Solid Black":
#         background_details = "deep black seamless backdrop, dramatic contrast lighting"
#     elif background == "Transparent (Isolated)":
#         background_details = "isolated product and model on transparent background, alpha-style cutout look"
#     elif background in ("Workspace", "Office"):
#         background_details = "modern office interior, desk elements, soft natural window light"
#     elif background == "Professional Studio":
#         background_details = "high-end photography studio setup, softbox lighting, controlled environment"
#     elif background in ("City", "Urban"):
#         background_details = "urban city street background, modern architecture, outdoor natural lighting"
#     elif background in ("Historic", "Ancient"):
#         background_details = "historic architecture backdrop, textured stone walls, cinematic lighting"
#     elif background == "HomeVibe":
#         background_details = "adaptive home interior, kitchen for cookware, living room for furniture, dining for tableware, natural lighting, warm atmosphere"
#     elif background == "Custom Idea":
#         background_details = custom_background if custom_background else "custom conceptual background as described by user"
#     else:
#         print(f"DEBUG: No match found, using fallback for: '{background}'")
#         background_details = "urban city street background, modern architecture, outdoor natural lighting"
#     print(f"DEBUG dual: background_details='{background_details}'")

#     # Style preset
#     style_map = {
#         "Modern":     "clean lines, neutral tones, contemporary fashion styling",
#         "Minimalist": "simple composition, limited color palette, clean aesthetic",
#         "Vintage":    "warm tones, soft contrast, retro fashion mood",
#         "Monochrome": "single dominant color tone, controlled contrast",
#         "Aesthetic":  "trendy Instagram-style composition, soft glow lighting",
#         "Close-up":   "product emphasized but full body still visible",
#     }
#     style_details = style_map.get(style_preset, "natural styling")

#     # Studio / lighting
#     if studio_type == "Marketing Studio":
#         studio_details = (
#             "cinematic lighting, dramatic shadows, dynamic composition, "
#             "luxury brand storytelling, magazine-style campaign photography"
#         )
#     else:
#         studio_details = (
#             "clean commercial lighting, balanced exposure, "
#             "e-commerce catalog photography style"
#         )

#     # Apparel style
#     if apparel_style == "Professional":
#         apparel_details = "structured posture, confident stance, polished professional styling"
#     elif apparel_style == "Casual":
#         apparel_details = "relaxed pose, natural expression, casual lifestyle styling"
#     else:
#         apparel_details = "natural comfortable pose"

#     # Category -> framing + composition + pose/camera variations
#     cat = category.lower()

#     # Face lock — defined first so all category blocks below can use it
#     face_lock = "The person from Image 1 must be reproduced exactly — identical face, skin tone, body, hair. "

#     if cat == "fashion":
#         dual_core         = (
#             face_lock +
#             "Image 2 = clothing/apparel — dress the person in this exact garment. "
#             "Match exact color, pattern, cut, fabric texture from Image 2. Natural fit, no design alterations."
#         )
#         framing_rules     = (
#             "full-body visible, head-to-toe framing, entire person inside frame, "
#             "feet clearly visible, no cropped body, no waist-up shot"
#         )
#         composition_style = "full-length fashion photograph"
#         variation_styles  = [
#             "candid street style, mid-stride walk, relaxed posture, soft gaze away from camera",
#             "asymmetrical editorial stance, weight on one hip, hand lightly resting on outfit, moody lookbook aesthetic",
#             "dynamic high-fashion posture, sharp shoulders, confident editorial expression, fluid body language",
#             "effortless leaning pose, subtle movement adjusting the garment, contemporary lifestyle vibe",
#         ]
#         variation_camera  = [
#             "85mm lens, professional full-body studio framing",
#             "slightly wider lens, campaign-style full-length framing",
#             "mid-distance lifestyle full-body composition",
#             "low-angle fashion photography perspective, full body in frame",
#         ]

#     elif cat == "accessories":
#         dual_core = (
#             face_lock +
#             "Image 2 = accessory — study its shape, structure, and form carefully to understand "
#             "what it is and which body part it naturally belongs on. "
#             "Place it on that exact body part with correct scale, correct orientation, and natural fit. "
#             "Reproduce every detail from Image 2 exactly — same color, texture, pattern, finish, proportions. "
#             "The accessory must be prominently visible and large enough in frame to see all its details clearly. "
#             "Never shrink, blur, or hide the accessory. Never substitute or invent anything not in Image 2."
#         )
#         framing_rules     = (
#             "Study Image 2 to determine the accessory and its body part, then choose the tightest framing "
#             "that shows the accessory clearly and prominently — it must fill enough of the frame to see every detail. "
#             "Face visible whenever the accessory is on the upper body. "
#             "Never use a distant or full-body shot for accessories."
#         )
#         composition_style = "close-up lifestyle accessory photograph"
#         variation_styles  = [
#             "accessory naturally worn on its correct body part, relaxed elegant pose, soft warm lighting, natural expression",
#             "casual lifestyle moment, accessory in natural worn position, authentic expression, accessory prominently in frame",
#             "confident pose, accessory clearly displayed on correct body part, polished styling, direct camera gaze",
#             "detail-focused composition, accessory sharp and prominent, sophisticated natural pose",
#         ]
#         variation_camera  = [
#             "close-up lens, tight framing on accessory and its worn body part, shallow depth of field",
#             "85mm lens, lifestyle close-up, accessory and face both sharp and prominent",
#             "macro-style framing, accessory fills frame, sharp detail, softly blurred background",
#             "portrait lens, accessory prominent and sharp, face naturally visible, detail-oriented composition",
#         ]

#     elif cat == "e-commerce":
#         dual_core         = (
#             face_lock +
#             "Image 2 = product — analyze its real-world function and show the person naturally using it "
#             "exactly as it is used in daily life. "
#             "Person's body angle, gaze direction, hands, and pose must authentically match the product interaction. "
#             "Full product visible, all edges inside frame, nothing cropped. "
#             "Exact product color, shape, texture, brand markings from Image 2 — unchanged. "
#             "Never substitute or add anything not in Image 2."
#         )
#         framing_rules     = (
#             "Medium close-up lifestyle framing, waist-up or chest-up. "
#             "Person's face and the product both clearly visible and in sharp focus. "
#             "Frame wide enough so entire product fits with all edges visible and nothing cut. "
#             "No distant full-body shots, no cropped heads."
#         )
#         composition_style = "premium commercial lifestyle portrait"
#         variation_styles  = [
#             "person deeply focused and naturally engaging with the product, realistic lifestyle home or workspace setting, elegant lighting",
#             "confident commercial portrait, person looking directly at camera while gracefully using or presenting the product",
#             "candid everyday lifestyle moment, person dynamically interacting with the product in a natural environment",
#             "lifestyle usage perspective, person actively operating or enjoying the product, sharp editorial styling",
#         ]
#         variation_camera  = [
#             "50mm lens, balanced chest-up composition showing person's interaction with the product",
#             "85mm portrait lens, tight framing on person's face and product details",
#             "medium close-up, sharp product focus, beautifully blurred background",
#             "cinematic commercial angle, dynamic depth of field emphasizing product in use",
#         ]

#     else:
#         dual_core         = (
#             face_lock +
#             "Image 2 = product — identify its real-world function from its shape and form, "
#             "then show the person using, holding, or wearing it exactly as it functions in real life. "
#             "Preserve exact product color, shape, label, texture unchanged. "
#             "Never substitute or add anything not in Image 2."
#         )
#         framing_rules     = "full-body visible, head-to-toe framing, entire person inside frame, feet clearly visible"
#         composition_style = "full-length fashion photograph"
#         variation_styles  = [
#             "candid street style, mid-stride walk, relaxed posture, soft gaze",
#             "asymmetrical editorial stance, weight on one hip, moody lookbook aesthetic",
#             "dynamic high-fashion posture, sharp shoulders, confident editorial expression",
#             "effortless leaning pose, adjusting garment, contemporary lifestyle vibe",
#         ]
#         variation_camera  = [
#             "85mm lens, professional studio framing",
#             "slightly wider lens, campaign-style framing",
#             "mid-distance lifestyle composition",
#             "low-angle fashion photography perspective",
#         ]

#     # Brand
#     brand_text        = f" by {brand_name}" if brand_name else ""
#     brand_instruction = f"showcasing {brand_name} brand identity, subtle branding visible, " if brand_name else ""

#     product_display = product_name if product_name.strip() else "the product"
#     additional_text = f", {additional_instructions}" if additional_instructions else ""

#     # Build prompts
#     prompts = []

#     for i in range(num_images):
#         pose_variation   = variation_styles[i % len(variation_styles)]
#         camera_variation = variation_camera[i % len(variation_camera)]

#         prompt = (
#             f"IMAGE 1 IS THE IDENTITY SOURCE — reproduce this exact person: same face, facial features, skin tone, body shape, clothing, hair. Do not generate a new person. Do not change the face. Do not change the clothes. "
#             f"Professional {composition_style} of {product_display}{brand_text}. "
#             f"{dual_core} "
#             f"{brand_instruction}"
#             f"If Image 2 shows a product set or multiple items, include ALL items in the scene — every item visible, none missing, exactly one of each, no duplicates. "
#             f"Background: {background_details}. "
#             f"Style: {style_details}. "
#             f"Lighting: {studio_details}. "
#             f"Pose: {apparel_details}, {pose_variation}. "
#             f"Camera: {camera_variation}. "
#             f"Framing: {framing_rules}. "
#             f"Sharp focus on person and product, balanced exposure, ultra realistic, 8k resolution, commercial photography quality."
#         )
#         prompts.append(truncate_prompt(prompt))

#     negative_prompt = (
#         "different person, changed face, new face, generated face, altered face, "
#         "different clothes, changed outfit, different clothing, "
#         "different skin tone, altered hair, different body type, "
#         "wrong product, substituted product, invented product, product cropped, "
#         "extra limbs, bad anatomy, blurry, low resolution, cartoon, cgi, "
#         "dark face, harsh shadows, overexposed background"
#     )

#     return prompts, negative_prompt

import base64
import os
import time
import uuid
from io import BytesIO
import requests
from PIL import Image
from app.config import APIFRAME_API_KEY, IMGBB_API_KEY
from app.gallery_meta import record_metadata

PROMPT_LIMIT = 4000  # safe limit for Flux 2 Pro
STATIC_DIR = "static"


async def image_to_pil(file):
    content = await file.read()
    return Image.open(BytesIO(content)).convert("RGB")


def save_image(pil_image):
    os.makedirs(STATIC_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join(STATIC_DIR, filename)
    pil_image.save(path, "PNG")
    return filename


def upload_image_to_imgbb(input_image: Image.Image) -> str:
     
    buffered = BytesIO()
    input_image.save(buffered, format="PNG")
    base64_image = base64.b64encode(buffered.getvalue()).decode()

    resp = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": IMGBB_API_KEY, "image": base64_image},
        timeout=60,
    )
    if resp.status_code != 200:
         
        raise Exception(f"imgbb upload failed: {resp.text}")

    url = resp.json().get("data", {}).get("url")
    if not url:
        raise Exception(f"No URL from imgbb: {resp.json()}")
    return url


MAX_POLLS = 100

def apiframe_dual_image_to_image(prompt: str, input_image: Image.Image, input_image_2: Image.Image):
    image_url_1 = upload_image_to_imgbb(input_image)
    image_url_2 = upload_image_to_imgbb(input_image_2)

    response = requests.post(
        "https://api.apiframe.ai/v2/images/generate",
        headers={"X-API-Key": APIFRAME_API_KEY, "Content-Type": "application/json"},
        json={
            "prompt": prompt,
            "model": "nano-banana",
            "nanoBananaParams": {"image_input": [image_url_1, image_url_2], "output_format": "png"}
        },
        timeout=120
    )
    response.raise_for_status()
    job_id = response.json().get("jobId")
    if not job_id:
        raise Exception(f"No jobId returned: {response.json()}")
    print(f"Job ID: {job_id}")

    for attempt in range(MAX_POLLS):
        # ✅ correct endpoint
        poll = requests.get(
            f"https://api.apiframe.ai/v2/jobs/{job_id}",
            headers={"X-API-Key": APIFRAME_API_KEY},
            timeout=30
        )
        poll.raise_for_status()
        data = poll.json()
        status = data.get("status")
        print(f"[{attempt+1}/{MAX_POLLS}] Status: {status} ({data.get('progress')}%)")

        if status in ("QUEUED", "PROCESSING"):
            time.sleep(3)
        elif status == "FAILED":
            raise Exception(f"Generation failed: {data.get('error')}")
        elif status == "COMPLETED":
            # ✅ correct parsing
            images = (data.get("result") or {}).get("images")
            if not images:
                raise Exception(f"No images returned: {data}")
            img_resp = requests.get(images[0], timeout=60)
            img_resp.raise_for_status()
            return Image.open(BytesIO(img_resp.content)).convert("RGB")
        else:
            print(f"Unknown status '{status}', retrying...")
            time.sleep(3)

    raise Exception(f"Job timed out after {MAX_POLLS * 3}s")

def get_apiframe_job(job_id: str, api_key: str):

    response = requests.get(
        f"https://api.apiframe.ai/v2/jobs/{job_id}",
        headers={
            "X-API-Key": api_key
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    # Job still running
    if data.get("status") != "COMPLETED":
        return data

    # Download image
    image_url = data["result"]["images"][0]

    img_resp = requests.get(image_url, timeout=60)
    img_resp.raise_for_status()

    image = Image.open(BytesIO(img_resp.content)).convert("RGB")

    filename = save_image(image)

    return {
        "status": data["status"],
        "job_id": job_id,
        "image_url": image_url,
        "filename": filename,
        "download_url": f"/static/{filename}"
    }
# async def generate_dual_image(prompt: str, negative_prompt: str, file, file_2):
#     try:
#         input_image = await image_to_pil(file)
#         input_image_2 = await image_to_pil(file_2)
#         image = apiframe_dual_image_to_image(prompt, input_image, input_image_2)
#         filename = save_image(image)
#         return {"status": "success", "filename": filename, "provider": "apiframe"}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}
import asyncio

async def generate_dual_image(
    prompt: str,
    negative_prompt: str,
    file,
    file_2,
    product_name: str = None,
    brand_name: str = None,
    category: str = None,
    studio_type: str = None,
):
    try:
        input_image = await image_to_pil(file)
        input_image_2 = await image_to_pil(file_2)
        loop = asyncio.get_event_loop()
        image = await loop.run_in_executor(
            None, apiframe_dual_image_to_image, prompt, input_image, input_image_2
        )
        filename = save_image(image)
        record_metadata(
            filename,
            product_name=product_name,
            brand_name=brand_name,
            category=category,
            studio_type=studio_type,
        )
        return {"status": "success", "filename": filename, "provider": "apiframe"}
    except Exception as e:
        return {"status": "error", "message": str(e)}



def truncate_prompt(text: str, max_chars: int = PROMPT_LIMIT) -> str:
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars].rsplit(' ', 1)[0].rstrip(', ')
    print(f"⚠️  PROMPT TRUNCATED: {len(text)} → {len(truncated)} chars (limit={max_chars})")
    return truncated




 
def build_dual_prompt(
    studio_type,
    category,
    target_audience,
    product_name,
    brand_name,
    background,
    style_preset,
    apparel_style=None,
    num_images=1,
    custom_background=None,
    additional_instructions=""
):
    """
    Dual-image Product-on-Person prompt builder.
    Image 1 (input_image)   = user's own photo — person is the base.
    Image 2 (input_image_2) = product photo   — AI detects type and places it.
    Supports 1-4 stylistic variations.
    """

    if num_images < 1 or num_images > 4:
        raise ValueError("num_images must be between 1 and 4")

    # Sanitise free text
    product_name            = product_name.strip()[:80]
    brand_name              = brand_name.strip()[:40]
    additional_instructions = additional_instructions.strip()[:150]
    if custom_background:
        custom_background = custom_background.strip()[:100]

    # Background
    print(f"DEBUG dual: background='{background}'")
    background = background.strip()
    if background == "Solid White":
        background_details = "clean white seamless backdrop, shadow under feet, studio floor visible"
    elif background == "Solid Black":
        background_details = "deep black seamless backdrop, dramatic contrast lighting"
    elif background == "Transparent (Isolated)":
        background_details = "isolated product and model on transparent background, alpha-style cutout look"
    elif background in ("Workspace", "Office"):
        background_details = "modern office interior, desk elements, soft natural window light"
    elif background == "Professional Studio":
        background_details = "high-end photography studio setup, softbox lighting, controlled environment"
    elif background in ("City", "Urban"):
        background_details = "urban city street background, modern architecture, outdoor natural lighting"
    elif background in ("Historic", "Ancient"):
        background_details = "historic architecture backdrop, textured stone walls, cinematic lighting"
    elif background == "HomeVibe":
        background_details = "adaptive home interior, kitchen for cookware, living room for furniture, dining for tableware, natural lighting, warm atmosphere"
    elif background == "Custom Idea":
        background_details = custom_background if custom_background else "custom conceptual background as described by user"
    else:
        print(f"DEBUG: No match found, using fallback for: '{background}'")
        background_details = "urban city street background, modern architecture, outdoor natural lighting"
    print(f"DEBUG dual: background_details='{background_details}'")

    # Style preset
    style_map = {
        "Modern":     "clean lines, neutral tones, contemporary fashion styling",
        "Minimalist": "simple composition, limited color palette, clean aesthetic",
        "Vintage":    "warm tones, soft contrast, retro fashion mood",
        "Monochrome": "single dominant color tone, controlled contrast",
        "Aesthetic":  "trendy Instagram-style composition, soft glow lighting",
        "Close-up":   "product emphasized but full body still visible",
    }
    style_details = style_map.get(style_preset, "natural styling")

    # Studio / lighting
    if studio_type == "Marketing Studio":
        studio_details = (
            "cinematic lighting, dramatic shadows, dynamic composition, "
            "luxury brand storytelling, magazine-style campaign photography"
        )
    else:
        studio_details = (
            "clean commercial lighting, balanced exposure, "
            "e-commerce catalog photography style"
        )

    # Apparel style
    if apparel_style == "Professional":
        apparel_details = "structured posture, confident stance, polished professional styling"
    elif apparel_style == "Casual":
        apparel_details = "relaxed pose, natural expression, casual lifestyle styling"
    else:
        apparel_details = "natural comfortable pose"

    # Category -> framing + composition + pose/camera variations
    cat = category.lower()

    # Face lock — defined first so all category blocks below can use it
    face_lock = "The person from Image 1 must be reproduced exactly — identical face, skin tone, body, hair. "

    if cat == "fashion":
        dual_core         = (
            face_lock +
            "Image 2 = clothing/apparel — dress the person in this exact garment. "
            "Match exact color, pattern, cut, fabric texture from Image 2. Natural fit, no design alterations."
        )
        framing_rules     = (
            "full-body visible, head-to-toe framing, entire person inside frame, "
            "feet clearly visible, no cropped body, no waist-up shot"
        )
        composition_style = "full-length fashion photograph"
        variation_styles  = [
            "candid street style, mid-stride walk, relaxed posture, soft gaze away from camera",
            "asymmetrical editorial stance, weight on one hip, hand lightly resting on outfit, moody lookbook aesthetic",
            "dynamic high-fashion posture, sharp shoulders, confident editorial expression, fluid body language",
            "effortless leaning pose, subtle movement adjusting the garment, contemporary lifestyle vibe",
        ]
        variation_camera  = [
            "85mm lens, professional full-body studio framing",
            "slightly wider lens, campaign-style full-length framing",
            "mid-distance lifestyle full-body composition",
            "low-angle fashion photography perspective, full body in frame",
        ]

    elif cat == "accessories":
        dual_core = (
            face_lock +
            "Image 2 = accessory — study its shape, structure, and form carefully to understand "
            "what it is and which body part it naturally belongs on. "
            "Place it on that exact body part with correct scale, correct orientation, and natural fit. "
            "Reproduce every detail from Image 2 exactly — same color, texture, pattern, finish, proportions. "
            "The accessory must be prominently visible and large enough in frame to see all its details clearly. "
            "Never shrink, blur, or hide the accessory. Never substitute or invent anything not in Image 2."
        )
        framing_rules     = (
            "Study Image 2 to determine the accessory and its body part, then choose the tightest framing "
            "that shows the accessory clearly and prominently — it must fill enough of the frame to see every detail. "
            "Face visible whenever the accessory is on the upper body. "
            "Never use a distant or full-body shot for accessories."
        )
        composition_style = "close-up lifestyle accessory photograph"
        variation_styles  = [
            "accessory naturally worn on its correct body part, relaxed elegant pose, soft warm lighting, natural expression",
            "casual lifestyle moment, accessory in natural worn position, authentic expression, accessory prominently in frame",
            "confident pose, accessory clearly displayed on correct body part, polished styling, direct camera gaze",
            "detail-focused composition, accessory sharp and prominent, sophisticated natural pose",
        ]
        variation_camera  = [
            "close-up lens, tight framing on accessory and its worn body part, shallow depth of field",
            "85mm lens, lifestyle close-up, accessory and face both sharp and prominent",
            "macro-style framing, accessory fills frame, sharp detail, softly blurred background",
            "portrait lens, accessory prominent and sharp, face naturally visible, detail-oriented composition",
        ]

    elif cat == "e-commerce":
        dual_core         = (
            face_lock +
            "Image 2 = product — analyze its real-world function and show the person naturally using it "
            "exactly as it is used in daily life. "
            "Person's body angle, gaze direction, hands, and pose must authentically match the product interaction. "
            "Full product visible, all edges inside frame, nothing cropped. "
            "Exact product color, shape, texture, brand markings from Image 2 — unchanged. "
            "Never substitute or add anything not in Image 2."
        )
        framing_rules     = (
            "Medium close-up lifestyle framing, waist-up or chest-up. "
            "Person's face and the product both clearly visible and in sharp focus. "
            "Frame wide enough so entire product fits with all edges visible and nothing cut. "
            "No distant full-body shots, no cropped heads."
        )
        composition_style = "premium commercial lifestyle portrait"
        variation_styles  = [
            "person deeply focused and naturally engaging with the product, realistic lifestyle home or workspace setting, elegant lighting",
            "confident commercial portrait, person looking directly at camera while gracefully using or presenting the product",
            "candid everyday lifestyle moment, person dynamically interacting with the product in a natural environment",
            "lifestyle usage perspective, person actively operating or enjoying the product, sharp editorial styling",
        ]
        variation_camera  = [
            "50mm lens, balanced chest-up composition showing person's interaction with the product",
            "85mm portrait lens, tight framing on person's face and product details",
            "medium close-up, sharp product focus, beautifully blurred background",
            "cinematic commercial angle, dynamic depth of field emphasizing product in use",
        ]

    else:
        dual_core         = (
            face_lock +
            "Image 2 = product — identify its real-world function from its shape and form, "
            "then show the person using, holding, or wearing it exactly as it functions in real life. "
            "Preserve exact product color, shape, label, texture unchanged. "
            "Never substitute or add anything not in Image 2."
        )
        framing_rules     = "full-body visible, head-to-toe framing, entire person inside frame, feet clearly visible"
        composition_style = "full-length fashion photograph"
        variation_styles  = [
            "candid street style, mid-stride walk, relaxed posture, soft gaze",
            "asymmetrical editorial stance, weight on one hip, moody lookbook aesthetic",
            "dynamic high-fashion posture, sharp shoulders, confident editorial expression",
            "effortless leaning pose, adjusting garment, contemporary lifestyle vibe",
        ]
        variation_camera  = [
            "85mm lens, professional studio framing",
            "slightly wider lens, campaign-style framing",
            "mid-distance lifestyle composition",
            "low-angle fashion photography perspective",
        ]

    # Brand
    brand_text        = f" by {brand_name}" if brand_name else ""
    brand_instruction = f"showcasing {brand_name} brand identity, subtle branding visible, " if brand_name else ""

    product_display = product_name if product_name.strip() else "the product"
    additional_text = f", {additional_instructions}" if additional_instructions else ""

    # Build prompts
    prompts = []

    for i in range(num_images):
        pose_variation   = variation_styles[i % len(variation_styles)]
        camera_variation = variation_camera[i % len(variation_camera)]

        prompt = (
            f"IMAGE 1 IS THE IDENTITY SOURCE — reproduce this exact person: same face, facial features, skin tone, body shape, clothing, hair. Do not generate a new person. Do not change the face. Do not change the clothes. "
            f"Professional {composition_style} of {product_display}{brand_text}. "
            f"{dual_core} "
            f"{brand_instruction}"
            f"If Image 2 shows a product set or multiple items, include ALL items in the scene — every item visible, none missing, exactly one of each, no duplicates. "
            f"Background: {background_details}. "
            f"Style: {style_details}. "
            f"Lighting: {studio_details}. "
            f"Pose: {apparel_details}, {pose_variation}. "
            f"Camera: {camera_variation}. "
            f"Framing: {framing_rules}. "
            f"Sharp focus on person and product, balanced exposure, ultra realistic, 8k resolution, commercial photography quality."
        )
        prompts.append(truncate_prompt(prompt))

    negative_prompt = (
        "different person, changed face, new face, generated face, altered face, "
        "different clothes, changed outfit, different clothing, "
        "different skin tone, altered hair, different body type, "
        "wrong product, substituted product, invented product, product cropped, "
        "extra limbs, bad anatomy, blurry, low resolution, cartoon, cgi, "
        "dark face, harsh shadows, overexposed background"
    )

    return prompts, negative_prompt