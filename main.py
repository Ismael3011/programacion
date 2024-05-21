from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta, date, time
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from db.client import db_client
from schemas.productos import producto_schema, productos_schema
from bson import ObjectId

class Productos(BaseModel):
    id : str | None
    nombre : str
    descripcion : str
    precio : float
    categoria : str
    stock : int

app = FastAPI()

#LISTAR PRODUCTOS
@app.get("/productos")
async def productos():
    return productos_schema(db_client.local.productos.find())

#CREAR PRODUCTOS
@app.post("/productos")
async def producto(producto : Productos):
    if type (buscardb("nombre",producto.nombre)) == Productos:
       raise HTTPException(status_code=400, detail="Ya hay productos con ese nombre.")
    
    producto_dict = dict(producto)
    del producto_dict["id"]

    id = db_client.local.productos.insert_one(producto_dict).inserted_id

    new_producto = producto_schema(db_client.local.productos.find_one({"_id" : id}))

    return Productos(**new_producto)

#ELIMINAR PRODUCTOS
@app.delete("/productos/{id}")
async def producto(id : str):

    found = db_client.local.productos.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code=400, detail="No hay usuarios con esa ID para eliminar.")
    
    return {"Bien" : "Se eliminó el prodcuto."}

# ACTUALIZAR PRODUCTOS
@app.put("/productos")
async def actualizar_producto(producto: Productos):
    producto_dict = dict(producto)
    del producto_dict["id"]

    try:
        db_client.local.productos.find_one_and_replace(
            {"_id" : ObjectId(producto.id)}, producto_dict)
    except:
        return{"Error" : "No se encotró el producto"}
    return buscardb("_id", ObjectId(producto.id))
#BUSCAR POR ID
@app.get("/productos/{id}")
async def producto(id :str):
    return buscardb("_id", ObjectId(id))

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
    
def buscardb(field : str, key):
    try:
        producto = db_client.local.productos.find_one({field : key})
        return Productos(**producto_schema(producto))
    except :
        return {"error" : "No se encontró el usuario"}
    