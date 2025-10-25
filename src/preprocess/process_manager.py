def procesar_lista_productos(productos):
    """
    Limpia y prepara los datos de productos antes de mostrarlos.
    """
    if not productos:
        return []

    productos_limpios = []
    for p in productos:
        producto = {
            "id": p.get("id", "N/A"),
            "name": p.get("name", "Sin nombre"),
            "description": p.get("description", "Sin descripción"),
            "feature": p.get("feature", "Sin características"),
            "price": p.get("price", 0),
            "imageUrl": p.get("imageUrl", None),
            "createdAt": p.get("createdAt", "Desconocido")
        }
        productos_limpios.append(producto)

    return productos_limpios


def mostrar_productos_en_consola(productos):
    """
    Muestra los productos en formato legible por consola.
    """
    if not productos:
        print("\n--- Resultados ---")
        print("No se encontraron productos con esos criterios.\n")
        return

    print("\n--- Resultados ---")
    for p in productos:
        print(f"""
🆔 ID: {p['id']}
📦 Nombre: {p['name']}
📝 Descripción: {p['description']}
✨ Características: {p['feature']}
💰 Precio: ${p['price']}
🖼️ Imagen: {p['imageUrl']}
📅 Fecha de creación: {p['createdAt']}
----------------------------------------
""")
