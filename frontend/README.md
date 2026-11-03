# LUMIÈRE STUDIO — Frontend

A React (Vite) wizard UI for your FastAPI "LUMIÈRE STUDIO" backend, styled after
studio.arvora.ai's 5-step create flow: **Choose Studio → Upload → Customize → Add Details → Generate**.

## 1. Run the backend first

From your `lumiere-studio` project folder:

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Confirm it's up: open `http://127.0.0.1:8000` — you should see
`{"message": "LUMIÈRE STUDIO Running"}`.

## 2. Configure the frontend

```bash
cp .env.example .env
```

By default `.env` points `VITE_API_BASE_URL` at `http://127.0.0.1:8000`. Change this if your
backend runs elsewhere (a different port, a server IP, or a deployed domain).

## 3. Run the frontend

```bash
npm install
npm run dev -- --host

```

Open the URL Vite prints (usually `http://localhost:5173`).

## How the frontend talks to the backend (and why CORS isn't an issue)

Your backend already enables permissive CORS in `app/main.py`:

```python
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
```

That means the browser is allowed to call the FastAPI server directly from a different
origin (e.g. `localhost:5173` → `localhost:8000`), which is what this frontend does by
default via `src/api/client.js`, using `VITE_API_BASE_URL` as the base URL for every request.

If you'd rather the browser never make a cross-origin request at all during development
(e.g. your backend sits behind a stricter network policy later), switch to the built-in dev
proxy instead — no code changes needed:

```bash
# .env
VITE_API_BASE_URL=/api
VITE_BACKEND_ORIGIN=http://127.0.0.1:8000
```

`vite.config.js` forwards anything under `/api/*` and `/static/*` to `VITE_BACKEND_ORIGIN`
on Vite's own dev server, so requests never leave `localhost:5173` from the browser's point
of view. (This proxy only runs during `npm run dev` — for a production build, serve the
frontend behind a reverse proxy such as Nginx if you want the same effect, or just keep
using Option A with CORS.)

## Endpoints this frontend calls

| Endpoint | Used for | Fields |
|---|---|---|
| `POST /generate` | Photo Studio / Marketing Studio (single product image, optional AI model) | `file`, `product_name`, `brand_name`, `studio_type`, `category`, `target_audience`, `region`, `apparel_style`, `style_preset`, `background`, `num_images`, `custom_background`, `additional_instructions` |
| `POST /generate-dual` | Custom Model Studio (your own model photo + product photo) | `own_image`, `product_image`, `product_name`, `brand_name`, `studio_type`, `category`, `target_audience`, `apparel_style`, `style_preset`, `background`, `num_images`, `custom_background`, `additional_instructions` |

All option values (backgrounds, style presets, regions, etc.) in the UI match exactly what
`app/service.py` and `app/dual_img.py` expect — sending anything else falls back to a
generic default server-side.

## Known backend quirk worth fixing

`app/route.py` returns the generated image location as a hardcoded absolute URL:

```python
"download_url": f"http://localhost:8000/static/{filename}",
```

That's fine on your own machine, but it will point to the wrong host once the backend is
deployed anywhere else. This frontend works around it (`resolveAssetUrl` in
`src/api/client.js` rewrites the host to match whatever `VITE_API_BASE_URL` you configured),
but the cleaner long-term fix is to build the URL from the incoming request instead, e.g.:

```python
from fastapi import Request

@router.post("/generate")
async def generate(request: Request, ...):
    ...
    return {"status": "completed", "download_url": str(request.base_url) + f"static/{filename}"}
```

## Security note on your `.env`

Your uploaded backend `.env` contains live API keys (Hugging Face, imgbb, APIFrame,
Butterfly, and a webhook token). Keep that file on the server only — never ship it to the
frontend or a public repo, and consider rotating those keys since they were shared in this
conversation.

## Project structure

```
src/
  api/client.js          axios instance + resolveAssetUrl + generateImage/generateDualImage
  components/
    Stepper.jsx           left-hand progress rail
    StudioStep.jsx         step 1: studio type + category
    UploadStep.jsx         step 2: image upload(s), audience, region
    CustomizeStep.jsx      step 3: background, style, apparel, variations
    DetailsStep.jsx        step 4: product/brand name, instructions
    ResultStep.jsx          step 5: summary, generate, result/download
  App.jsx                 wizard state + navigation
  App.css / index.css    design tokens + layout
```
