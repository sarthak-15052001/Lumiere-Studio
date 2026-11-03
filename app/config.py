
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = "black-forest-labs/FLUX.2-dev"
HF_PROVIDER = "fal-ai"


IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
APIFRAME_API_KEY = os.getenv("APIFRAME_API_KEY")
BUTTERFLY_API_KEY = os.getenv("BUTTERFLY_API_KEY")