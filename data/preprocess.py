import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series, DataFrame
from utils.logger import log_info, log_warning


# 🧩 Validación de esquema para usuarios
class UserSchema(pa.DataFrameModel):
    id: Series[str]
    name: Series[str]
    email: Series[str]
    puntos: Series[int] = pa.Field(ge=0, nullable=True)
    createdAt: Series[pd.Timestamp] = pa.Field(nullable=True)  # ✅ tu dataset usa camelCase

    class Config:
        coerce = True  # fuerza tipos correctos automáticamente


# 🧩 Validación de esquema para productos
class ProductSchema(pa.DataFrameModel):
    id: Series[str]
    name: Series[str]
    description: Series[str] = pa.Field(nullable=True)
    feature: Series[str] = pa.Field(nullable=True)
    price: Series[float] = pa.Field(ge=0, nullable=True)
    imageUrl: Series[str] = pa.Field(nullable=True)
    createdAt: Series[pd.Timestamp] = pa.Field(nullable=True)

    class Config:
        coerce = True


# 🧠 Función de preprocesamiento de usuarios
def preprocess_users(users_data):
    df = pd.DataFrame(users_data)

    if df.empty:
        log_warning("⚠️ No hay datos de usuarios.")
        return df

    # ✅ Alinear nombres de columnas con el esquema (camelCase)
    if "created_at" in df.columns and "createdAt" not in df.columns:
        df.rename(columns={"created_at": "createdAt"}, inplace=True)

    # ⚙️ Crear columnas faltantes
    if "puntos" not in df.columns:
        log_warning("Columna 'puntos' no encontrada. Se asignará valor 0 por defecto.")
        df["puntos"] = 0

    if "createdAt" not in df.columns:
        log_warning("Columna 'createdAt' no encontrada. Se asignará valor nulo.")
        df["createdAt"] = None

    # 🧮 Asegurar tipo numérico en puntos
    df["puntos"] = pd.to_numeric(df["puntos"], errors="coerce").fillna(0).astype(int)

    # 🕒 Asegurar tipo fecha en createdAt
    df["createdAt"] = pd.to_datetime(df["createdAt"], errors="coerce")

    # 🧾 Validar con Pandera
    try:
        validated: DataFrame[UserSchema] = UserSchema.validate(df)
        log_info(f"✅ Datos de usuarios validados correctamente. ({len(df)} registros)")
        return validated
    except pa.errors.SchemaError as e:
        log_warning(f"❌ Error de validación en usuarios: {e}")
        return df


# 🧠 Función de preprocesamiento de productos
def preprocess_products(products_data):
    df = pd.DataFrame(products_data)

    if df.empty:
        log_warning("⚠️ No hay datos de productos.")
        return df

    # ✅ Alinear nombres de columnas con el esquema
    if "created_at" in df.columns and "createdAt" not in df.columns:
        df.rename(columns={"created_at": "createdAt"}, inplace=True)

    # ⚙️ Crear columnas faltantes
    if "price" not in df.columns:
        log_warning("Columna 'price' no encontrada. Se asignará valor 0 por defecto.")
        df["price"] = 0.0

    if "createdAt" not in df.columns:
        log_warning("Columna 'createdAt' no encontrada. Se asignará valor nulo.")
        df["createdAt"] = None

    # 💰 Convertir precio a numérico
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)

    # 🕒 Asegurar tipo fecha
    df["createdAt"] = pd.to_datetime(df["createdAt"], errors="coerce")

    # 🧾 Validar con Pandera
    try:
        validated: DataFrame[ProductSchema] = ProductSchema.validate(df)
        log_info(f"✅ Datos de productos validados correctamente. ({len(df)} registros)")
        return validated
    except pa.errors.SchemaError as e:
        log_warning(f"❌ Error de validación en productos: {e}")
        return df
