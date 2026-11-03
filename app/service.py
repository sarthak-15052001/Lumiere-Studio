# import base64
# import requests,time
# import uuid
# import os
# from PIL import Image
# from io import BytesIO
# from app.config import APIFRAME_API_KEY, IMGBB_API_KEY,BUTTERFLY_API_KEY

# STATIC_DIR = "static"
# PROMPT_LIMIT = 3000


# # ---------- PROMPT LIMIT ----------
# def truncate_prompt(text: str, max_chars: int = PROMPT_LIMIT) -> str:
#     if len(text) <= max_chars:
#         return text
#     return text[:max_chars].rsplit(" ", 1)[0]


# # ---------- IMAGE TO PIL ----------
# async def image_to_pil(file):
#     content = await file.read()
#     return Image.open(BytesIO(content)).convert("RGB")


# # ---------- SAVE IMAGE ----------
# def save_image(pil_image):
#     os.makedirs(STATIC_DIR, exist_ok=True)
#     filename = f"{uuid.uuid4().hex}.png"
#     path = os.path.join(STATIC_DIR, filename)
#     pil_image.save(path, "PNG")
#     return filename
# def image_to_base64(image: Image.Image):
#     buffered = BytesIO()
#     image.save(buffered, format="PNG")
#     return base64.b64encode(buffered.getvalue()).decode()

# def upload_image_to_imgbb(input_image: Image.Image) -> str:
     
#     buffered = BytesIO()
#     input_image.save(buffered, format="PNG")
#     base64_image = base64.b64encode(buffered.getvalue()).decode()

#     resp = requests.post(
#         "https://api.imgbb.com/1/upload",
#         data={"key": IMGBB_API_KEY, "image": base64_image},
#         timeout=60
#     )
#     if resp.status_code != 200:
         
#         raise Exception(f"imgbb upload failed: {resp.text}")

#     url = resp.json().get("data", {}).get("url")
#     if not url:
#         raise Exception(f"No URL from imgbb: {resp.json()}")
#     return url

# MAX_POLLS = 100  # ~5 min at 3s intervals

# def apiframe_image_to_image(prompt: str, input_image: Image.Image):
#     image_url = upload_image_to_imgbb(input_image)

#     response = requests.post(
#         "https://api.apiframe.ai/v2/images/generate",
#         headers={"X-API-Key": APIFRAME_API_KEY, "Content-Type": "application/json"},
#         json={
#             "prompt": prompt,
#             "model": "nano-banana",
#             "nanoBananaParams": {"image_input": [image_url], "output_format": "png"}
#         },
#         timeout=120
#     )
#     response.raise_for_status()
#     job_id = response.json()["jobId"]
#     print(f"Job ID: {job_id}")

#     for attempt in range(MAX_POLLS):
#         # ✅ correct endpoint: /v2/jobs/:id (NOT /v2/images/{job_id})
#         poll = requests.get(
#             f"https://api.apiframe.ai/v2/jobs/{job_id}",
#             headers={"X-API-Key": APIFRAME_API_KEY},
#             timeout=30
#         )
#         poll.raise_for_status()
#         data = poll.json()
#         status = data.get("status")
#         progress = data.get("progress")
#         print(f"[{attempt+1}/{MAX_POLLS}] Status: {status} ({progress}%)")

#         if status in ("QUEUED", "PROCESSING"):
#             time.sleep(3)
#         elif status == "FAILED":
#             raise Exception(f"Generation failed: {data.get('error')}")
#         elif status == "COMPLETED":
#             # ✅ correct parsing: result -> images
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
#         }
#     )

#     response.raise_for_status()

#     data = response.json()

#     if data.get("status") != "COMPLETED":
#         return data

#     image_url = data["result"]["images"][0]

#     image = requests.get(image_url)

#     image.raise_for_status()

#     pil_image = Image.open(BytesIO(image.content)).convert("RGB")

#     filename = save_image(pil_image)

#     return {
#         "status": "COMPLETED",
#         "job_id": job_id,
#         "image_url": image_url,
#         "filename": filename,
#         "download_url": f"http://localhost:8000/static/{filename}"
#     }


# import asyncio

# async def generate_image(prompt: str, negative_prompt: str, file) -> dict:

#     try:
#         input_image = await image_to_pil(file)

#         print("\n================ PROMPT ================\n")
#         print(prompt)

#         print("\n============== NEGATIVE PROMPT ==============\n")
#         print(negative_prompt)

#         print("\n===========================================\n")
#         loop = asyncio.get_event_loop()
#         image = await loop.run_in_executor(
#             None, apiframe_image_to_image, prompt, input_image
#         )
#         filename = save_image(image)
#         return {"status": "success", "filename": filename, "provider": "apiframe"}

#     except Exception as e:
#         return {
#             "status": "error",
#             "message": str(e)
#         }
     

 
# def build_prompt(
#     studio_type,
#     category,
#     target_audience,
#     product_name,
#     brand_name,
#     background,
#     style_preset,
#     apparel_style=None,
#     num_images=1,
#     model_region="Indian",
#     custom_background=None,
#     additional_instructions=""
# ):
#     """
#     Structured Product-to-Life FULL BODY enforced prompt builder
#     Supports 1–4 stylistic variations.
#     """

#     # ===============================
#     # VALIDATE IMAGE COUNT
#     # ===============================
#     if num_images < 1 or num_images > 4:
#         raise ValueError("num_images must be between 1 and 4")

#     # ===============================
#     # SANITISE USER-SUPPLIED FREE TEXT
#     # ===============================
#     product_name            = product_name.strip()[:120]
#     brand_name              = brand_name.strip()[:60]
#     additional_instructions = additional_instructions.strip()[:200]
#     if custom_background:
#         custom_background = custom_background.strip()[:150]

#     ethnicity_map = {
#         "Indian": "Indian ethnicity, natural Indian facial features, brown skin tone, South Asian appearance",
#         "Western": "European features, fair skin tone",
#         "East Asian": "East Asian facial features",
#         "Middle Eastern": "Middle Eastern features"
#     }

#     if model_region == "None":
#         ethnicity_details = ""
#     else:
#         ethnicity_details = ethnicity_map.get(model_region, "")

#     # ===============================
#     # BACKGROUND LOGIC
#     # ===============================
#     print(f"DEBUG: Background value received: '{background}'")
#     background = background.strip()

#     if background == "Solid White":
#         background_details = "clean white seamless backdrop, shadow under feet, studio floor visible"
#     elif background == "Solid Black":
#         background_details = "deep black seamless backdrop, dramatic contrast lighting"
#     elif background == "Transparent (Isolated)":
#         background_details = "isolated product and model on transparent background, alpha-style cutout look"
#     elif background == "Workspace":
#         background_details = "modern office interior, desk elements, soft natural window light"
#     elif background == "Office":
#         background_details = "modern office interior, desk elements, soft natural window light"
#     elif background == "Professional Studio":
#         background_details = "high-end photography studio setup, softbox lighting, controlled environment"
#     elif background == "City":
#         background_details = "urban city street background, modern architecture, outdoor natural lighting"
#     elif background == "Urban":
#         background_details = "urban city street background, modern architecture, outdoor natural lighting"
#     elif background == "Historic":
#         background_details = "historic architecture backdrop, textured stone walls, cinematic lighting"
#     elif background == "Ancient":
#         background_details = "historic architecture backdrop, textured stone walls, cinematic lighting"
#     elif background == "HomeVibe":
#         background_details = "adaptive home interior, kitchen for cookware, living room for furniture, dining for tableware, natural lighting, warm atmosphere"
#     elif background == "Custom Idea":
#         background_details = custom_background if custom_background else "custom conceptual background as described by user"
#     else:
#         print(f"DEBUG: No match found, using fallback for: '{background}'")
#         background_details = "urban city street background, modern architecture, outdoor natural lighting"

#     print(f"DEBUG: Final background_details: '{background_details}'")

#     # ===============================
#     # STYLE PRESET LOGIC
#     # ===============================
#     style_map = {
#         "Modern": "clean lines, neutral tones, contemporary fashion styling",
#         "Minimalist": "simple composition, limited color palette, clean aesthetic",
#         "Vintage": "warm tones, soft contrast, retro fashion mood",
#         "Monochrome": "single dominant color tone, controlled contrast",
#         "Aesthetic": "trendy Instagram-style composition, soft glow lighting",
#         "Close-up": "product emphasized but full body still visible"
#     }
#     style_details = style_map.get(style_preset, "natural styling")

#     # ===============================
#     # STUDIO LOGIC
#     # ===============================
#     if model_region == "None":
#         if studio_type == "Marketing Studio":
#             studio_details = (
#                 "cinematic lighting, dramatic shadows, dynamic composition, "
#                 "luxury brand storytelling, artistic still-life arrangement"
#             )
#         else:
#             studio_details = (
#                 "clean commercial product lighting, balanced exposure, "
#                 "pristine e-commerce product photography style"
#             )
#     else:
#         if studio_type == "Marketing Studio":
#             studio_details = (
#                 "cinematic lighting, dramatic shadows, dynamic composition, "
#                 "luxury brand storytelling, magazine-style campaign photography"
#             )
#         else:
#             studio_details = (
#                 "clean commercial lighting, balanced exposure, "
#                 "e-commerce catalog photography style"
#             )

#     # ===============================
#     # APPAREL STYLE LOGIC
#     # ===============================
#     if apparel_style == "Professional":
#         apparel_details = "structured posture, confident stance, polished styling"
#     elif apparel_style == "Casual":
#         apparel_details = "relaxed pose, natural expression, lifestyle styling"
#     else:
#         apparel_details = "natural fashion pose"

#     # ===============================
#     # CATEGORY LOGIC
#     # ===============================
#     if category.lower() == "fashion":
#         interaction_logic = "product properly worn with realistic fit and natural fabric folds"
#     elif category.lower() == "accessories":
#         interaction_logic = "product clearly visible and proportionally accurate while being worn or held naturally"
#     else:
#         interaction_logic = "product naturally integrated and visually accurate"

#     # ===============================
#     # JEWELRY MANNEQUIN LOGIC
#     # ===============================
#     is_jewelry = (target_audience.lower() in ["jewellary", "jewelry", "Jewelry"] and model_region == "None")

#     if category.lower() == "accessories" and is_jewelry and model_region == "None":
#         interaction_logic = (
#             "Visually detect jewelry type from image → "
#             "ring/bracelet/bangle: white or black resin display hand+wrist ONLY. "
#             "earrings/necklace/nose ring/set: white or black fashion mannequin head with realistic face (closed eyes, nose, lips), full rounded head, ears visible, neck below."
#         )
#         framing_rules = (
#             "white or black matte fashion mannequin head, realistic facial features (eyes, nose, lips), full round dome visible, "
#             "both ears shown, chin and neck below. NO head cropping. Only uploaded jewelry. Clean studio."
#         )
#         composition_style = "professional jewelry display on elegant fashion display figurine"
#     elif model_region == "None":
#         interaction_logic = "product positioned with artistic freedom, creative centering variations, showcasing artistic details and innovative presentations"
#         framing_rules = (
#             "creative shot compositions, artistic framing freedom, innovative product presentation, "
#             "no humans, no body parts, no hands, artistic environment freedom, "
#             "creative product styling with artistic liberty"
#         )
#         composition_style = "professional still-life product photography"
#     elif category.lower() == "fashion":
#         interaction_logic = "product properly worn with realistic fit and natural fabric folds"
#         framing_rules = (
#             "full-body visible, head-to-toe framing, entire person inside frame, "
#             "feet clearly visible, no cropped body, no waist-up shot"
#         )
#         composition_style = "full-length fashion photograph"
#     elif category.lower() == "accessories":
#         interaction_logic = (
#             "Visually analyze the product image and identify what type of accessory it is. "
#             "Reason about which specific body part it is designed to be worn on in real life. "
#             "Place it only on that correct body part — anatomically accurate, correctly scaled, naturally worn."
#         )
#         framing_rules = (
#             "Automatically determine the best framing based on the detected accessory type: "
#             "crop tightly around the body part where the accessory is worn so it is clearly visible and in sharp focus. "
#             "Show the model's face if the accessory is near the head or neck. "
#             "No unnecessary full-body shots — frame intelligently to highlight the accessory on its correct location."
#         )
#         composition_style = "close-up lifestyle accessory photograph, placement auto-detected from product image"
#     elif category.lower() == "e-commerce":
#         interaction_logic = (
#             "Analyze the product and determine its real-world function. "
#             "Show the model naturally using, wearing, or interacting with the product in the way it is actually used in daily life. "
#             "The interaction must feel authentic and contextually accurate to the product type."
#         )
#         framing_rules = (
#             "medium close-up lifestyle photography, waist-up or chest-up framing, "
#             "model's face and the product both clearly visible and in sharp focus, "
#             "dynamic natural interaction, perfectly scaled product, no distant full-body shots, no cropped heads"
#         )
#         composition_style = "premium commercial lifestyle portrait"
#     else:
#         interaction_logic = "product naturally integrated and visually accurate"
#         framing_rules = (
#             "full-body visible, head-to-toe framing, entire person inside frame, "
#             "feet clearly visible, no cropped body, no waist-up shot"
#         )
#         composition_style = "full-length fashion photograph"

#     # ===============================
#     # PRODUCT PRESERVATION
#     # ===============================
#     if model_region == "None":
#         uniqueness_rule = "different camera perspectives and diverse product angles, " if num_images > 1 else ""
#         preservation_rules = (
#             "CRITICAL: preserve product design, color, shape and texture accurately. "
#             "STRICTLY follow the requested background environment and style preset. "
#             "different camera perspectives and diverse product angles, maintain professional still-life staging, "
#             "ensure the product is centered and presented beautifully, product positioned as a standalone hero object, "
#             "perfectly centered, showing fine details, "
#         )
#     else:
#         preservation_rules = (
#             "CRITICAL: preserve exact original product color, do not alter or change product color in any way, "
#             "maintain identical product design, exact shape, accurate proportions, "
#             "preserve original material texture, correct stitching patterns, "
#             "keep original product appearance unchanged, no color modification, no redesign, "
#             "product must match reference image exactly"
#         )

#     brand_text = f" by {brand_name}" if brand_name else ""
#     brand_instruction = f"Showcasing the premium identity of {brand_name}, featuring subtle {brand_name} branding and logos if applicable, high-end commercial appeal, " if brand_name else ""

#     # ===============================
#     # VARIATION LOGIC (1–4)
#     # ===============================
#     if model_region == "None":
#         if category.lower() == "accessories" and is_jewelry:
#             variation_styles = [
#                 "elegant random-colored display figure, correct jewelry-matching body part, high-end editorial styling",
#                 "upright uniquely-colored display figure, front-facing naturally scaled to accessory, premium catalog",
#                 "creative asymmetrical random-colored display figure, dramatic shadow play, unique artistic pose",
#                 "expressive randomly-colored display figure, elegant gesture, aesthetic editorial jewelry photography"
#             ]
#             variation_camera = [
#                 "50mm lens, medium composition showing display figure and accessory clearly, clean catalog styling",
#                 "85mm lens, balanced composition showing display figure and jewelry, soft background blur",
#                 "35mm lens, wide enough to frame full display figure (NOT cropped), editorial product styling",
#                 "portrait lens, elegant showcase of display figure and accessory, full figure uncropped"
#             ]
#         else:
#             variation_styles = [
#                 "perfectly level product placement, eye-level perspective, clean studio arrangement",
#                 "slight 45 degree angle view, showing depth and dimensions of the product, professional staging",
#                 "top-down flat-lay style, artistic arrangement with subtle props, high-end catalog look",
#                 "dramatic side profile, emphasizing silhouette and texture, artistic lighting shadows"
#             ]
#             variation_camera = [
#                 "100mm macro lens, sharp product focus, hero shot, centered composition, product-only framing",
#                 "50mm lens, balanced product photography, hero shot, centered composition, product-only framing",
#                 "top-down architectural framing, hero shot, centered composition, product-only framing",
#                 "85mm lens, dramatic lighting setup, hero shot, centered composition, product-only framing"
#             ]
#     elif category.lower() == "accessories":
#         variation_styles = [
#             "natural relaxed pose, accessory naturally worn on its correct body part, elegant subtle gesture",
#             "casual lifestyle moment, accessory in natural worn position, soft authentic expression",
#             "confident pose, accessory prominently displayed on correct body part, polished professional styling",
#             "close detail emphasis, accessory in sharp focus on its worn location, sophisticated composition",
#         ]
#         variation_camera = [
#             "macro lens, tight close-up framing on the accessory and its worn body part",
#             "85mm lens, lifestyle close-up composition showing accessory in context",
#             "shallow depth of field, accessory in sharp focus, background softly blurred",
#             "detail-oriented portrait composition, sharp accessory and face focus",
#         ]
#     elif category.lower() == "e-commerce":
#         variation_styles = [
#             "model naturally engaging with the product based on its real-world use, realistic lifestyle setting, elegant lighting",
#             "confident commercial portrait, model looking directly at camera while gracefully using or presenting the product",
#             "candid everyday lifestyle moment, model dynamically interacting with the product in a natural environment",
#             "lifestyle usage perspective, model actively enjoying or operating the product, sharp editorial styling",
#         ]
#         variation_camera = [
#             "50mm lens, balanced chest-up composition showing model's interaction with the product",
#             "85mm portrait lens, tight framing focusing on model's face and product details",
#             "medium close-up, sharp focus on product usage with beautifully blurred background",
#             "cinematic commercial angle, dynamic depth of field emphasizing the product in use",
#         ]
#     else:
#         variation_styles = [
#             "candid street style movement, mid-stride fashion walk, relaxed posture with a soft gaze away from the camera",
#             "asymmetrical editorial stance, weight shifted casually to one hip, hand lightly resting on the apparel, moody lookbook aesthetic",
#             "dynamic high-fashion posture, sharp shoulders, looking over the shoulder with a confident editorial expression, fluid body language",
#             "effortless leaning pose, subtle candid movement adjusting the garment, contemporary lifestyle fashion vibe"
#         ]
#         variation_camera = [
#             "85mm lens, professional studio framing",
#             "slightly wider lens, campaign-style framing",
#             "mid-distance lifestyle composition",
#             "low-angle fashion photography perspective"
#         ]

#     prompts = []
#     product_display = product_name if product_name.strip() else "the product"
#     additional_text = f", {additional_instructions}" if additional_instructions else ""

#     for i in range(num_images):
#         pose_variation = variation_styles[i % len(variation_styles)]
#         camera_variation = variation_camera[i % len(variation_camera)]

#         if model_region == "None":
#             prompt = (
#                 f"Professional still-life product photography of {product_display}{brand_text}, "
#                 f"same design, same color, same shape, "
#                 f"{brand_instruction}"
#                 f"{preservation_rules}, "
#                 f"{interaction_logic}, "
#                 f"{framing_rules}, "
#                 f"{background_details}, "
#                 f"{studio_details}, "
#                 f"{style_details}, "
#                 f"{pose_variation}, "
#                 f"{camera_variation}, "
#                 f"sharp focus, extremely detailed textures, high dynamic range, "
#                 f"ultra realistic, 8k resolution, commercial advertising quality{additional_text}"
#             )
#             prompts.append(truncate_prompt(prompt))
#         elif category.lower() == "e-commerce":
#             prompt = (
#                 f"Professional interior design and commercial product photography of {product_display}{brand_text}, "
#                 f"{brand_instruction}"
#                 f"featuring a real {ethnicity_details} model interacting naturally with the product, "
#                 f"product placed realistically in a natural Indian home or lifestyle environment, "
#                 f"{preservation_rules}, "
#                 f"product beautifully displayed resting naturally on a solid surface or floor in a realistic setting, "
#                 f"{background_details}, "
#                 f"{studio_details}, "
#                 f"{style_details}, "
#                 f"{pose_variation}, "
#                 f"{camera_variation}, "
#                 f"still-life architectural photography, purely product-focused, exquisite pristine staging, "
#                 f"perfect scale and proportions, highly detailed room environment, "
#                 f"sharp focus, depth of field, high dynamic range, "
#                 f"ultra realistic, 8k resolution{additional_text}"
#             )
#             prompts.append(truncate_prompt(prompt))
#         else:
#             prompt = (
#                 f"Professional full-length fashion photograph of a {ethnicity_details} {target_audience} model "
#                 f"wearing {product_name}{brand_text}, "
#                 f"{brand_instruction}"
#                 f"{preservation_rules}, "
#                 f"{interaction_logic}, "
#                 f"{apparel_details}, "
#                 f"{background_details}, "
#                 f"{studio_details}, "
#                 f"{style_details}, "
#                 f"{pose_variation}, "
#                 f"{camera_variation}, "
#                 f"{framing_rules}, "
#                 f"model centered in frame, realistic skin texture, "
#                 f"sharp focus, depth of field, high dynamic range, "
#                 f"ultra realistic, 8k resolution, professional commercial product photography{additional_text}"
#             )
#             prompts.append(truncate_prompt(prompt))

#     negative_prompt = (
#         "half body, cropped body, cut off feet, waist up shot, hollow head, open top mannequin, missing top of head, bowl head, vase head, planter head mannequin, sliced head mannequin, hollow bust, incomplete mannequin head, headless retail display, faceless, decapitated, headless necklace bust, jewelry display stand without head, neck only dummy, headless jewelry bust, "
#         "extra limbs, extra fingers, bad anatomy, distorted product, "
#         "floating product, blurry, low resolution, cartoon style, cgi look"
#     )

#     return prompts, negative_prompt

import base64
import requests,time
import uuid
import os
from PIL import Image
from io import BytesIO
from app.config import APIFRAME_API_KEY, IMGBB_API_KEY,BUTTERFLY_API_KEY
from app.gallery_meta import record_metadata

STATIC_DIR = "static"
PROMPT_LIMIT = 3000


# ---------- PROMPT LIMIT ----------
def truncate_prompt(text: str, max_chars: int = PROMPT_LIMIT) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0]


# ---------- IMAGE TO PIL ----------
async def image_to_pil(file):
    content = await file.read()
    return Image.open(BytesIO(content)).convert("RGB")


# ---------- SAVE IMAGE ----------
def save_image(pil_image):
    os.makedirs(STATIC_DIR, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join(STATIC_DIR, filename)
    pil_image.save(path, "PNG")
    return filename
def image_to_base64(image: Image.Image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def upload_image_to_imgbb(input_image: Image.Image) -> str:
     
    buffered = BytesIO()
    input_image.save(buffered, format="PNG")
    base64_image = base64.b64encode(buffered.getvalue()).decode()

    resp = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": IMGBB_API_KEY, "image": base64_image},
        timeout=60
    )
    if resp.status_code != 200:
         
        raise Exception(f"imgbb upload failed: {resp.text}")

    url = resp.json().get("data", {}).get("url")
    if not url:
        raise Exception(f"No URL from imgbb: {resp.json()}")
    return url

MAX_POLLS = 100  # ~5 min at 3s intervals

def apiframe_image_to_image(prompt: str, input_image: Image.Image):
    image_url = upload_image_to_imgbb(input_image)

    response = requests.post(
        "https://api.apiframe.ai/v2/images/generate",
        headers={"X-API-Key": APIFRAME_API_KEY, "Content-Type": "application/json"},
        json={
            "prompt": prompt,
            "model": "nano-banana",
            "nanoBananaParams": {"image_input": [image_url], "output_format": "png"}
        },
        timeout=120
    )
    response.raise_for_status()
    job_id = response.json()["jobId"]
    print(f"Job ID: {job_id}")

    for attempt in range(MAX_POLLS):
        # ✅ correct endpoint: /v2/jobs/:id (NOT /v2/images/{job_id})
        poll = requests.get(
            f"https://api.apiframe.ai/v2/jobs/{job_id}",
            headers={"X-API-Key": APIFRAME_API_KEY},
            timeout=30
        )
        poll.raise_for_status()
        data = poll.json()
        status = data.get("status")
        progress = data.get("progress")
        print(f"[{attempt+1}/{MAX_POLLS}] Status: {status} ({progress}%)")

        if status in ("QUEUED", "PROCESSING"):
            time.sleep(3)
        elif status == "FAILED":
            raise Exception(f"Generation failed: {data.get('error')}")
        elif status == "COMPLETED":
            # ✅ correct parsing: result -> images
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
        }
    )

    response.raise_for_status()

    data = response.json()

    if data.get("status") != "COMPLETED":
        return data

    image_url = data["result"]["images"][0]

    image = requests.get(image_url)

    image.raise_for_status()

    pil_image = Image.open(BytesIO(image.content)).convert("RGB")

    filename = save_image(pil_image)

    return {
        "status": "COMPLETED",
        "job_id": job_id,
        "image_url": image_url,
        "filename": filename,
        "download_url": f"http://localhost:8000/static/{filename}"
    }

def butterfly_image_to_image(prompt: str, negative_prompt: str, input_image: Image.Image):
    image_url = upload_image_to_imgbb(input_image)

    response = requests.post(
        'https://butterflyapi.com/api/v1/run',
        headers={
            'Authorization': f'Bearer {BUTTERFLY_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            'api': 'image-to-image',
            'input': {
                'image_url': image_url,
                'prompt': prompt,
                'strength': 0.4,
                'negative_prompt': negative_prompt,
            },
        },
        timeout=120
    )

    if response.status_code != 200:
         
        raise Exception(response.text)

    job_id = response.json().get('jobId')
    if not job_id:
        raise Exception(f"No jobId: {response.json()}")

    for _ in range(60):
        time.sleep(5)
         
        poll = requests.get(
            f'https://butterflyapi.com/api/v1/status/{job_id}',
            headers={'Authorization': f'Bearer {BUTTERFLY_API_KEY}'},
            timeout=30
        )
        data = poll.json()
        status = data.get('status')

        if status == 'completed':
            output_url = data.get('output')
            if not output_url:
                raise Exception(f"No output URL: {data}")
            img_resp = requests.get(output_url, timeout=60)
            img_resp.raise_for_status()
            return Image.open(BytesIO(img_resp.content)).convert('RGB')

        elif status == 'failed':
            raise Exception(f"Butterfly job failed: {data.get('error')}")

    raise Exception("Butterfly job timed out")


import asyncio

async def generate_image(
    prompt: str,
    negative_prompt: str,
    file,
    product_name: str = None,
    brand_name: str = None,
    category: str = None,
    studio_type: str = None,
) -> dict:

    try:
        input_image = await image_to_pil(file)

        print("\n================ PROMPT ================\n")
        print(prompt)

        print("\n============== NEGATIVE PROMPT ==============\n")
        print(negative_prompt)

        print("\n===========================================\n")
        loop = asyncio.get_event_loop()
        image = await loop.run_in_executor(
            None, apiframe_image_to_image, prompt, input_image
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
        return {
            "status": "error",
            "message": str(e)
        }
     

 
def build_prompt(
    studio_type,
    category,
    target_audience,
    product_name,
    brand_name,
    background,
    style_preset,
    apparel_style=None,
    num_images=1,
    model_region="Indian",
    custom_background=None,
    additional_instructions=""
):
    """
    Structured Product-to-Life FULL BODY enforced prompt builder
    Supports 1–4 stylistic variations.
    """

    # ===============================
    # VALIDATE IMAGE COUNT
    # ===============================
    if num_images < 1 or num_images > 4:
        raise ValueError("num_images must be between 1 and 4")

    # ===============================
    # SANITISE USER-SUPPLIED FREE TEXT
    # ===============================
    product_name            = product_name.strip()[:120]
    brand_name              = brand_name.strip()[:60]
    additional_instructions = additional_instructions.strip()[:200]
    if custom_background:
        custom_background = custom_background.strip()[:150]

    ethnicity_map = {
        "Indian": "Indian ethnicity, natural Indian facial features, brown skin tone, South Asian appearance",
        "Western": "European features, fair skin tone",
        "East Asian": "East Asian facial features",
        "Middle Eastern": "Middle Eastern features"
    }

    if model_region == "None":
        ethnicity_details = ""
    else:
        ethnicity_details = ethnicity_map.get(model_region, "")

    # ===============================
    # BACKGROUND LOGIC
    # ===============================
    print(f"DEBUG: Background value received: '{background}'")
    background = background.strip()

    if background == "Solid White":
        background_details = "clean white seamless backdrop, shadow under feet, studio floor visible"
    elif background == "Solid Black":
        background_details = "deep black seamless backdrop, dramatic contrast lighting"
    elif background == "Transparent (Isolated)":
        background_details = "isolated product and model on transparent background, alpha-style cutout look"
    elif background == "Workspace":
        background_details = "modern office interior, desk elements, soft natural window light"
    elif background == "Office":
        background_details = "modern office interior, desk elements, soft natural window light"
    elif background == "Professional Studio":
        background_details = "high-end photography studio setup, softbox lighting, controlled environment"
    elif background == "City":
        background_details = "urban city street background, modern architecture, outdoor natural lighting"
    elif background == "Urban":
        background_details = "urban city street background, modern architecture, outdoor natural lighting"
    elif background == "Historic":
        background_details = "historic architecture backdrop, textured stone walls, cinematic lighting"
    elif background == "Ancient":
        background_details = "historic architecture backdrop, textured stone walls, cinematic lighting"
    elif background == "HomeVibe":
        background_details = "adaptive home interior, kitchen for cookware, living room for furniture, dining for tableware, natural lighting, warm atmosphere"
    elif background == "Custom Idea":
        background_details = custom_background if custom_background else "custom conceptual background as described by user"
    else:
        print(f"DEBUG: No match found, using fallback for: '{background}'")
        background_details = "urban city street background, modern architecture, outdoor natural lighting"

    print(f"DEBUG: Final background_details: '{background_details}'")

    # ===============================
    # STYLE PRESET LOGIC
    # ===============================
    style_map = {
        "Modern": "clean lines, neutral tones, contemporary fashion styling",
        "Minimalist": "simple composition, limited color palette, clean aesthetic",
        "Vintage": "warm tones, soft contrast, retro fashion mood",
        "Monochrome": "single dominant color tone, controlled contrast",
        "Aesthetic": "trendy Instagram-style composition, soft glow lighting",
        "Close-up": "product emphasized but full body still visible"
    }
    style_details = style_map.get(style_preset, "natural styling")

    # ===============================
    # STUDIO LOGIC
    # ===============================
    if model_region == "None":
        if studio_type == "Marketing Studio":
            studio_details = (
                "cinematic lighting, dramatic shadows, dynamic composition, "
                "luxury brand storytelling, artistic still-life arrangement"
            )
        else:
            studio_details = (
                "clean commercial product lighting, balanced exposure, "
                "pristine e-commerce product photography style"
            )
    else:
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

    # ===============================
    # APPAREL STYLE LOGIC
    # ===============================
    if apparel_style == "Professional":
        apparel_details = "structured posture, confident stance, polished styling"
    elif apparel_style == "Casual":
        apparel_details = "relaxed pose, natural expression, lifestyle styling"
    else:
        apparel_details = "natural fashion pose"

    # ===============================
    # CATEGORY LOGIC
    # ===============================
    if category.lower() == "fashion":
        interaction_logic = "product properly worn with realistic fit and natural fabric folds"
    elif category.lower() == "accessories":
        interaction_logic = "product clearly visible and proportionally accurate while being worn or held naturally"
    else:
        interaction_logic = "product naturally integrated and visually accurate"

    # ===============================
    # JEWELRY MANNEQUIN LOGIC
    # ===============================
    is_jewelry = (target_audience.lower() in ["jewellary", "jewelry", "Jewelry"] and model_region == "None")

    if category.lower() == "accessories" and is_jewelry and model_region == "None":
        interaction_logic = (
            "Visually detect jewelry type from image → "
            "ring/bracelet/bangle: white or black resin display hand+wrist ONLY. "
            "earrings/necklace/nose ring/set: white or black fashion mannequin head with realistic face (closed eyes, nose, lips), full rounded head, ears visible, neck below."
        )
        framing_rules = (
            "white or black matte fashion mannequin head, realistic facial features (eyes, nose, lips), full round dome visible, "
            "both ears shown, chin and neck below. NO head cropping. Only uploaded jewelry. Clean studio."
        )
        composition_style = "professional jewelry display on elegant fashion display figurine"
    elif model_region == "None":
        interaction_logic = "product positioned with artistic freedom, creative centering variations, showcasing artistic details and innovative presentations"
        framing_rules = (
            "creative shot compositions, artistic framing freedom, innovative product presentation, "
            "no humans, no body parts, no hands, artistic environment freedom, "
            "creative product styling with artistic liberty"
        )
        composition_style = "professional still-life product photography"
    elif category.lower() == "fashion":
        interaction_logic = "product properly worn with realistic fit and natural fabric folds"
        framing_rules = (
            "full-body visible, head-to-toe framing, entire person inside frame, "
            "feet clearly visible, no cropped body, no waist-up shot"
        )
        composition_style = "full-length fashion photograph"
    elif category.lower() == "accessories":
        interaction_logic = (
            "Visually analyze the product image and identify what type of accessory it is. "
            "Reason about which specific body part it is designed to be worn on in real life. "
            "Place it only on that correct body part — anatomically accurate, correctly scaled, naturally worn."
        )
        framing_rules = (
            "Automatically determine the best framing based on the detected accessory type: "
            "crop tightly around the body part where the accessory is worn so it is clearly visible and in sharp focus. "
            "Show the model's face if the accessory is near the head or neck. "
            "No unnecessary full-body shots — frame intelligently to highlight the accessory on its correct location."
        )
        composition_style = "close-up lifestyle accessory photograph, placement auto-detected from product image"
    elif category.lower() == "e-commerce":
        interaction_logic = (
            "Analyze the product and determine its real-world function. "
            "Show the model naturally using, wearing, or interacting with the product in the way it is actually used in daily life. "
            "The interaction must feel authentic and contextually accurate to the product type."
        )
        framing_rules = (
            "medium close-up lifestyle photography, waist-up or chest-up framing, "
            "model's face and the product both clearly visible and in sharp focus, "
            "dynamic natural interaction, perfectly scaled product, no distant full-body shots, no cropped heads"
        )
        composition_style = "premium commercial lifestyle portrait"
    else:
        interaction_logic = "product naturally integrated and visually accurate"
        framing_rules = (
            "full-body visible, head-to-toe framing, entire person inside frame, "
            "feet clearly visible, no cropped body, no waist-up shot"
        )
        composition_style = "full-length fashion photograph"

    # ===============================
    # PRODUCT PRESERVATION
    # ===============================
    if model_region == "None":
        uniqueness_rule = "different camera perspectives and diverse product angles, " if num_images > 1 else ""
        preservation_rules = (
            "CRITICAL: preserve product design, color, shape and texture accurately. "
            "STRICTLY follow the requested background environment and style preset. "
            "different camera perspectives and diverse product angles, maintain professional still-life staging, "
            "ensure the product is centered and presented beautifully, product positioned as a standalone hero object, "
            "perfectly centered, showing fine details, "
        )
    else:
        preservation_rules = (
            "CRITICAL: preserve exact original product color, do not alter or change product color in any way, "
            "maintain identical product design, exact shape, accurate proportions, "
            "preserve original material texture, correct stitching patterns, "
            "keep original product appearance unchanged, no color modification, no redesign, "
            "product must match reference image exactly"
        )

    brand_text = f" by {brand_name}" if brand_name else ""
    brand_instruction = f"Showcasing the premium identity of {brand_name}, featuring subtle {brand_name} branding and logos if applicable, high-end commercial appeal, " if brand_name else ""

    # ===============================
    # VARIATION LOGIC (1–4)
    # ===============================
    if model_region == "None":
        if category.lower() == "accessories" and is_jewelry:
            variation_styles = [
                "elegant random-colored display figure, correct jewelry-matching body part, high-end editorial styling",
                "upright uniquely-colored display figure, front-facing naturally scaled to accessory, premium catalog",
                "creative asymmetrical random-colored display figure, dramatic shadow play, unique artistic pose",
                "expressive randomly-colored display figure, elegant gesture, aesthetic editorial jewelry photography"
            ]
            variation_camera = [
                "50mm lens, medium composition showing display figure and accessory clearly, clean catalog styling",
                "85mm lens, balanced composition showing display figure and jewelry, soft background blur",
                "35mm lens, wide enough to frame full display figure (NOT cropped), editorial product styling",
                "portrait lens, elegant showcase of display figure and accessory, full figure uncropped"
            ]
        else:
            variation_styles = [
                "perfectly level product placement, eye-level perspective, clean studio arrangement",
                "slight 45 degree angle view, showing depth and dimensions of the product, professional staging",
                "top-down flat-lay style, artistic arrangement with subtle props, high-end catalog look",
                "dramatic side profile, emphasizing silhouette and texture, artistic lighting shadows"
            ]
            variation_camera = [
                "100mm macro lens, sharp product focus, hero shot, centered composition, product-only framing",
                "50mm lens, balanced product photography, hero shot, centered composition, product-only framing",
                "top-down architectural framing, hero shot, centered composition, product-only framing",
                "85mm lens, dramatic lighting setup, hero shot, centered composition, product-only framing"
            ]
    elif category.lower() == "accessories":
        variation_styles = [
            "natural relaxed pose, accessory naturally worn on its correct body part, elegant subtle gesture",
            "casual lifestyle moment, accessory in natural worn position, soft authentic expression",
            "confident pose, accessory prominently displayed on correct body part, polished professional styling",
            "close detail emphasis, accessory in sharp focus on its worn location, sophisticated composition",
        ]
        variation_camera = [
            "macro lens, tight close-up framing on the accessory and its worn body part",
            "85mm lens, lifestyle close-up composition showing accessory in context",
            "shallow depth of field, accessory in sharp focus, background softly blurred",
            "detail-oriented portrait composition, sharp accessory and face focus",
        ]
    elif category.lower() == "e-commerce":
        variation_styles = [
            "model naturally engaging with the product based on its real-world use, realistic lifestyle setting, elegant lighting",
            "confident commercial portrait, model looking directly at camera while gracefully using or presenting the product",
            "candid everyday lifestyle moment, model dynamically interacting with the product in a natural environment",
            "lifestyle usage perspective, model actively enjoying or operating the product, sharp editorial styling",
        ]
        variation_camera = [
            "50mm lens, balanced chest-up composition showing model's interaction with the product",
            "85mm portrait lens, tight framing focusing on model's face and product details",
            "medium close-up, sharp focus on product usage with beautifully blurred background",
            "cinematic commercial angle, dynamic depth of field emphasizing the product in use",
        ]
    else:
        variation_styles = [
            "candid street style movement, mid-stride fashion walk, relaxed posture with a soft gaze away from the camera",
            "asymmetrical editorial stance, weight shifted casually to one hip, hand lightly resting on the apparel, moody lookbook aesthetic",
            "dynamic high-fashion posture, sharp shoulders, looking over the shoulder with a confident editorial expression, fluid body language",
            "effortless leaning pose, subtle candid movement adjusting the garment, contemporary lifestyle fashion vibe"
        ]
        variation_camera = [
            "85mm lens, professional studio framing",
            "slightly wider lens, campaign-style framing",
            "mid-distance lifestyle composition",
            "low-angle fashion photography perspective"
        ]

    prompts = []
    product_display = product_name if product_name.strip() else "the product"
    additional_text = f", {additional_instructions}" if additional_instructions else ""

    for i in range(num_images):
        pose_variation = variation_styles[i % len(variation_styles)]
        camera_variation = variation_camera[i % len(variation_camera)]

        if model_region == "None":
            prompt = (
                f"Professional still-life product photography of {product_display}{brand_text}, "
                f"same design, same color, same shape, "
                f"{brand_instruction}"
                f"{preservation_rules}, "
                f"{interaction_logic}, "
                f"{framing_rules}, "
                f"{background_details}, "
                f"{studio_details}, "
                f"{style_details}, "
                f"{pose_variation}, "
                f"{camera_variation}, "
                f"sharp focus, extremely detailed textures, high dynamic range, "
                f"ultra realistic, 8k resolution, commercial advertising quality{additional_text}"
            )
            prompts.append(truncate_prompt(prompt))
        elif category.lower() == "e-commerce":
            prompt = (
                f"Professional interior design and commercial product photography of {product_display}{brand_text}, "
                f"{brand_instruction}"
                f"featuring a real {ethnicity_details} model interacting naturally with the product, "
                f"product placed realistically in a natural Indian home or lifestyle environment, "
                f"{preservation_rules}, "
                f"product beautifully displayed resting naturally on a solid surface or floor in a realistic setting, "
                f"{background_details}, "
                f"{studio_details}, "
                f"{style_details}, "
                f"{pose_variation}, "
                f"{camera_variation}, "
                f"still-life architectural photography, purely product-focused, exquisite pristine staging, "
                f"perfect scale and proportions, highly detailed room environment, "
                f"sharp focus, depth of field, high dynamic range, "
                f"ultra realistic, 8k resolution{additional_text}"
            )
            prompts.append(truncate_prompt(prompt))
        else:
            prompt = (
                f"Professional full-length fashion photograph of a {ethnicity_details} {target_audience} model "
                f"wearing {product_name}{brand_text}, "
                f"{brand_instruction}"
                f"{preservation_rules}, "
                f"{interaction_logic}, "
                f"{apparel_details}, "
                f"{background_details}, "
                f"{studio_details}, "
                f"{style_details}, "
                f"{pose_variation}, "
                f"{camera_variation}, "
                f"{framing_rules}, "
                f"model centered in frame, realistic skin texture, "
                f"sharp focus, depth of field, high dynamic range, "
                f"ultra realistic, 8k resolution, professional commercial product photography{additional_text}"
            )
            prompts.append(truncate_prompt(prompt))

    negative_prompt = (
        "half body, cropped body, cut off feet, waist up shot, hollow head, open top mannequin, missing top of head, bowl head, vase head, planter head mannequin, sliced head mannequin, hollow bust, incomplete mannequin head, headless retail display, faceless, decapitated, headless necklace bust, jewelry display stand without head, neck only dummy, headless jewelry bust, "
        "extra limbs, extra fingers, bad anatomy, distorted product, "
        "floating product, blurry, low resolution, cartoon style, cgi look"
    )

    return prompts, negative_prompt