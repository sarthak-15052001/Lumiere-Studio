from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.route import router
import os

app = FastAPI(title="LUMIÈRE STUDIO", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)

@app.get("/", tags=["Health"])
def home():
    return {"message": "LUMIÈRE STUDIO Running"}


# uvicorn app.main:app --host 0.0.0.0 --port 8000
# npm run dev -- --host
