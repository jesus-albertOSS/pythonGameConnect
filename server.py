from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Game Connect Backend")

# Ruta absoluta al reporte
REPORT_PATH = os.path.join(os.path.dirname(__file__), "reports", "reporte.html")

@app.get("/")
def home():
    return {"message": "🚀 Game Connect API funcionando"}

@app.get("/report")
def get_report():
    """
    Devuelve el reporte HTML generado.
    """
    if not os.path.exists(REPORT_PATH):
        return {"error": "Reporte no encontrado. Genera uno primero."}
    return FileResponse(REPORT_PATH, media_type="text/html")
