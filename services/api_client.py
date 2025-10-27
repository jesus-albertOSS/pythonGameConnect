import requests
from requests.auth import HTTPBasicAuth
from config.settings import API_URL, API_USER, API_PASS
from utils.logger import log_info, log_error

def get_data(endpoint: str):
    url = f"{API_URL}/api/{endpoint}"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(API_USER, API_PASS), timeout=10)
        response.raise_for_status()
        log_info(f"Datos obtenidos correctamente desde {endpoint}")
        return response.json()
    except requests.exceptions.RequestException as e:
        log_error(f"Error al obtener datos desde {endpoint}: {e}")
        return None
