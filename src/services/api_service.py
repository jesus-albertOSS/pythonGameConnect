import os
import base64
import requests
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# URL base de tu API en Render
BASE_URL = os.getenv("API_URL", "https://pi-backend2-ru4x.onrender.com/api/products")

# Credenciales de autenticación básica
USERNAME = os.getenv("API_USERNAME", "admin")
PASSWORD = os.getenv("API_PASSWORD", "admin123")

def obtener_productos():
    """Obtiene todos los productos desde la API remota usando autenticación básica"""
    try:
        # Crear el token base64 dinámicamente
        token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

        headers = {
            "accept": "application/json",
            "Authorization": f"Basic {token}",
        }

        response = requests.get(BASE_URL, headers=headers)

        print(f"\n📡 URL solicitada: {BASE_URL}")
        print(f"🔐 Auth: {USERNAME}:{PASSWORD}")
        print(f"🧾 Código de respuesta: {response.status_code}")

        if response.status_code == 200:
            print("✅ Productos obtenidos correctamente desde la API.\n")
            return response.json()
        else:
            print(f"⚠️ Error al obtener productos ({response.status_code}): {response.text}\n")
            return []
    except Exception as e:
        print("❌ Error de conexión con la API:", e)
        return []
