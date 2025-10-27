import pandas as pd
from utils.logger import log_info, log_warning

def preprocess_users(users_data):
    df = pd.DataFrame(users_data)

    if df.empty:
        log_warning("⚠️ No hay datos de usuarios.")
        return df

    # Si no existe 'puntos', la creamos con 0
    if "puntos" not in df.columns:
        log_warning("Columna 'puntos' no encontrada. Se asignará valor 0 por defecto.")
        df["puntos"] = 0

    # Convertir a número los puntos
    df["puntos"] = pd.to_numeric(df["puntos"], errors="coerce").fillna(0)

    # Procesar 'created_at' solo si existe
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    else:
        log_warning("Columna 'created_at' no encontrada. Se omitirá el procesamiento de fechas.")

    log_info(f"Datos de usuarios procesados correctamente. ({len(df)} registros)")
    return df


def preprocess_products(products_data):
    df = pd.DataFrame(products_data)

    if df.empty:
        log_warning("⚠️ No hay datos de productos.")
        return df

    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)
    else:
        log_warning("Columna 'price' no encontrada en productos.")

    log_info(f"Datos de productos procesados correctamente. ({len(df)} registros)")
    return df
