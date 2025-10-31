import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env dentro de la carpeta "env"
load_dotenv(dotenv_path="env/.env")

# Obtener las variables del entorno
API_URL = os.getenv("API_URL")
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")
