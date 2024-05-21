from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta, date, time
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext

app = FastAPI()

class Productos(BaseModel):
    id : int
    nombre : str
    descripcion : str
    precio : float
    categoria : str
    stock : int

productos_list = [Productos(id=1,nombre="Camiseta de algodón", descripcion= "Camiseta de manga corta", precio= 15.99, categoria= "Ropa", stock=100), 
                  Productos(id=2,nombre="Sudadera", descripcion= "Sudaderra con capucha", precio= 25.99, categoria= "Ropa", stock=90), ]

#LISTAR PRODUCTOS
@app.get("/productos")
async def productos():
    return productos_list

#CREAR PRODUCTOS
@app.post("/productos")
async def producto(producto : Productos):
    if type (product_search(producto.id)) == Productos:
        raise HTTPException(status_code=400, detail="Ya hay productos con esa ID.")
    else :
        productos_list.append(producto)
        return producto

#ELIMINAR PRODUCTOS
@app.delete("/productos/{id}")
async def producto(id : int):
    found = False

    for index, saved_product in enumerate(productos_list):
        if saved_product.id == id:
            del productos_list[index]
            found = True
            return {"Bien" : "Se eliminó correctamente"}
    if not found:
        raise HTTPException(status_code=400, detail="No hay usuarios con esa ID para eliminar.")

# ACTUALIZAR PRODUCTOS
@app.put("/productos/{id}")
async def actualizar_producto(id: int, producto: Productos):
    for index, saved_product in enumerate(productos_list):
        if saved_product.id == id:
            productos_list[index] = producto
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado para actualizar.")
#BUSCAR POR ID
@app.get("/productos/{id}")
async def producto(id :int):
    return product_search(id)

#BUSCAR POR NOMBRE
@app.get("/buscar")
async def producto(nombre :str):
    return product_search_name(nombre)

# BUSCAR PRODUCTOS POR CATEGORÍA
@app.get("/productos/categoria/{categoria}")
async def productos_por_categoria(categoria: str):
    resultados = []
    for product in productos_list:
        if categoria.lower() in product.categoria.lower():
            resultados.append(product)
    if len(resultados) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron productos en esa categoría")
    else:
        return list(resultados)
    
# ORDENAR PRODUCTOS POR PRECIO
@app.get("/ordenar")
async def ordenar_productos(orden: str):
    if orden == "ascendente":
        productos_ordenados = sorted(productos_list, key=lambda x: x.precio)
    elif orden =="descendente":
        productos_ordenados = sorted(productos_list, key=lambda x: x.precio, reverse=True)
    else:
        raise HTTPException(status_code=400, detail="El orden debe ser ascendente o descendente.")
    return productos_ordenados

# BORRAR PRODUCTOS POR CATEGORÍA
@app.delete("/productos/categoria/{categoria}/eliminar")
async def productos_por_categoria(categoria: str):
    global productos_list
    cont = 0
    listanueva = []
    for index, product in enumerate(productos_list):
        if categoria.lower() in product.categoria.lower():
            cont+=1
        else:
            listanueva.append(productos_list[index])

    if cont == 0:
        raise HTTPException(status_code=404, detail="No hay productos de esa categoria para eliminar.")
    else:
        productos_list = listanueva
        return {"Bien" : "Se eliminaros los productos de esa categoria."}
    
#FUNCIONES DE AYUDA
#BUSQUEDA DE PRODUCTOS
def product_search(id: int):
    productos = filter(lambda producto: producto.id==id, productos_list)
    try:
        return list(productos)[0]
    except:
        return {"error":"No se ha encontrado el producto"}
#BUSQUEDA DE PRODUCTOS POR NOMBRE
def product_search_name(nombre: str):
    productos = []
    for product in productos_list:
        if nombre.lower() in product.nombre.lower():
            productos.append(product)
    if len(productos)==0:
        return {"error":"No se ha encontrado el producto"}
    else:
        return list(productos)