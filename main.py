import subprocess
from services.api_client import get_data
from data.preprocess import preprocess_users, preprocess_products
from data.visualizacion import top_users_by_points, price_distribution
from utils.report_generator import generar_reporte_html  # usa tu versión gaming neón

def main():
    print("🚀 Iniciando análisis de Game Connect...")

    # 1️⃣ Obtener datos desde la API
    users_data = get_data("users")
    products_data = get_data("products")

    if not users_data or not products_data:
        print("❌ No se pudieron obtener los datos.")
        return

    # 2️⃣ Preprocesar datos
    df_users = preprocess_users(users_data)
    df_products = preprocess_products(products_data)

    # 3️⃣ Mostrar gráficos analíticos (opcional)
    if not df_users.empty:
        top_users_by_points(df_users)
    
    if not df_products.empty:
        price_distribution(df_products)

    # 4️⃣ Generar reporte HTML combinando ambos
    if not df_users.empty and not df_products.empty:
        generar_reporte_html(df_users, df_products)
        print("📄 Dashboard generado en 'reports/reporte.html'")

    print("✅ Análisis completado con éxito.")
    
    # 5️⃣ Levantar el servidor FastAPI automáticamente
    print("🚀 Iniciando servidor FastAPI en http://127.0.0.1:8000 ...")
    subprocess.run(["uvicorn", "server:app", "--reload", "--port", "8000"])

if __name__ == "__main__":
    main()
