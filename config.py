import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
LINK_2GIS = os.environ["LINK_2GIS"]
LINK_GOOGLE_MAPS = os.environ["LINK_GOOGLE_MAPS"]
PROXY_URL = os.environ.get("PROXY_URL", "")

PHOTOS_DIR = "photos/Astana/astana_photos"
RECORDS_PATH = "photos/Astana/photo_records.json"
