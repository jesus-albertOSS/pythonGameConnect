import pandas as pd
import pandera.pandas as pa
from pandera.typing import Series, DataFrame
from utils.logger import log_info, log_warning


class UserSchema(pa.DataFrameModel):
    id: Series[str]
    name: Series[str]
    email: Series[str]
    puntos: Series[int] = pa.Field(ge=0, nullable=True)
    createdAt: Series[pd.Timestamp] = pa.Field(nullable=True)

    class Config:
        coerce = True


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


def preprocess_users(users_data):
    df = pd.DataFrame(users_data)
    if df.empty:
        log_warning("⚠️ No hay datos de usuarios.")
        return df

    if "created_at" in df.columns and "createdAt" not in df.columns:
        df.rename(columns={"created_at": "createdAt"}, inplace=True)

    if "puntos" not in df.columns:
        log_warning("Columna 'puntos' no encontrada. Se asignará valor 0 por defecto.")
        df["puntos"] = 0

    if "createdAt" not in df.columns:
        log_warning("Columna 'createdAt' no encontrada. Se asignará valor nulo.")
        df["createdAt"] = None

    if df["puntos"].dtype == "object":
        log_warning("Algunos valores de 'puntos' no son numéricos. Se intentará convertirlos.")
    df["puntos"] = pd.to_numeric(df["puntos"], errors="coerce").fillna(0).astype(int)

    df["createdAt"] = pd.to_datetime(df["createdAt"], errors="coerce")

    if "name" in df.columns:
        df["name"] = df["name"].astype(str).str.strip().str.title()
    if "email" in df.columns:
        df["email"] = df["email"].astype(str).str.strip().str.lower()

    if df.duplicated(subset=["email"], keep="first").any():
        log_warning("Se encontraron usuarios duplicados por email. Se eliminarán duplicados.")
        df = df.drop_duplicates(subset=["email"], keep="first")

    try:
        validated: DataFrame[UserSchema] = UserSchema.validate(df)
        log_info(f"✅ Datos de usuarios validados correctamente. ({len(df)} registros)")
        return validated
    except pa.errors.SchemaError as e:
        log_warning(f"❌ Error de validación en usuarios: {e}")
        return df


def preprocess_products(products_data):
    df = pd.DataFrame(products_data)
    if df.empty:
        log_warning("⚠️ No hay datos de productos.")
        return df

    if "created_at" in df.columns and "createdAt" not in df.columns:
        df.rename(columns={"created_at": "createdAt"}, inplace=True)

    if "price" not in df.columns:
        log_warning("Columna 'price' no encontrada. Se asignará valor 0 por defecto.")
        df["price"] = 0.0

    if "createdAt" not in df.columns:
        log_warning("Columna 'createdAt' no encontrada. Se asignará valor nulo.")
        df["createdAt"] = None

    if df["price"].dtype == "object":
        log_warning("Algunos valores de 'price' no son numéricos. Se intentará convertirlos.")
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0)

    df["createdAt"] = pd.to_datetime(df["createdAt"], errors="coerce")

    if "name" in df.columns:
        df["name"] = df["name"].astype(str).str.strip().str.title()
    if "description" in df.columns:
        df["description"] = df["description"].astype(str).str.strip()
    if "feature" in df.columns:
        df["feature"] = df["feature"].astype(str).str.strip()

    if df.duplicated(subset=["name"], keep="first").any():
        log_warning("Se encontraron productos duplicados por nombre. Se eliminarán duplicados.")
        df = df.drop_duplicates(subset=["name"], keep="first")

    try:
        validated: DataFrame[ProductSchema] = ProductSchema.validate(df)
        log_info(f"✅ Datos de productos validados correctamente. ({len(df)} registros)")
        return validated
    except pa.errors.SchemaError as e:
        log_warning(f"❌ Error de validación en productos: {e}")
        return df
