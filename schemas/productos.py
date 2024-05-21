def producto_schema(producto):
    return {"id": str(producto["_id"]),
            "nombre": producto["nombre"],
            "descripcion": producto["descripcion"],
            "precio": producto["precio"],
            "categoria": producto["categoria"],
            "stock": producto["stock"]}

def productos_schema(productos):
    return [producto_schema(producto) for producto in productos]
        
