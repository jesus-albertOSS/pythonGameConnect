import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://pi-backend2-ru4x.onrender.com")
API_USER = os.getenv("API_USER", "admin")
API_PASS = os.getenv("API_PASS", "admin123")
