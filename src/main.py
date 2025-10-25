from services.api_service import obtener_productos
from preprocess.process_manager import procesar_lista_productos

# -------------------- FUNCIONES DE CONSULTA --------------------

def obtener_todos_los_productos():
    """Obtiene todos los productos desde la API"""
    productos = obtener_productos()
    return productos

def filtrar_productos(lista, nombre=None, precio_max=None):
    """Filtra una lista de productos descargada del backend"""
    filtrados = []
    for p in lista:
        nombre_ok = True
        precio_ok = True

        if nombre:
            nombre_ok = nombre.lower() in (p.get("name", "").lower())

        if precio_max:
            try:
                precio_ok = float(p.get("price", 0)) <= precio_max
            except (ValueError, TypeError):
                precio_ok = False

        if nombre_ok and precio_ok:
            filtrados.append(p)

    return filtrados

# -------------------- PROGRAMA PRINCIPAL --------------------

def main():
    print("=== Aplicación de Consulta de Productos (Render API) ===")
    print("1. Ver todos los productos")
    print("2. Filtrar productos")
    print("0. Salir")

    opcion = input("Selecciona una opción: ")

    productos = []
    if opcion == "1":
        productos = obtener_todos_los_productos()
    elif opcion == "2":
        nombre = input("Filtrar por nombre (dejar vacío si no): ") or None
        precio_str = input("Precio máximo (dejar vacío si no): ")
        precio_max = float(precio_str) if precio_str else None
        lista = obtener_todos_los_productos()
        productos = filtrar_productos(lista, nombre, precio_max)
    elif opcion == "0":
        print("Saliendo...")
        return
    else:
        print("Opción no válida.")
        return

    productos_procesados = procesar_lista_productos(productos)

    print("\n--- Resultados ---")
    if productos_procesados:
        for p in productos_procesados:
            print(f"{p['nombre']} - ${p['precio']} - {p['descripcion']}")
    else:
        print("No se encontraron productos con esos criterios.")

if __name__ == "__main__":
    main()
