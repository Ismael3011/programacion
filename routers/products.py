from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from pydantic import BaseModel
from db.client import db_client
from schemas.productos import producto_schema, productos_schema
from bson import ObjectId
from routers import users
from routers.users import auth_user, UserDB

router = APIRouter()

#ROUTERS
router.include_router(users.router)

class Productos(BaseModel):
    id : str | None
    nombre : str
    descripcion : str
    precio : float
    categoria : str
    stock : int

#ENDPOINTS
#LISTAR PRODUCTOS
@router.get("/productos")
async def productos():
    return productos_schema(db_client.local.productos.find())

#CREAR PRODUCTOS
@router.post("/productos")
async def producto(producto : Productos, user: UserDB = Depends(auth_user)):
    if type (buscardb("nombre",producto.nombre)) == Productos:
       raise HTTPException(status_code=400, detail="Ya hay productos con ese nombre.")
    
    producto_dict = dict(producto)
    del producto_dict["id"]

    id = db_client.local.productos.insert_one(producto_dict).inserted_id

    new_producto = producto_schema(db_client.local.productos.find_one({"_id" : id}))

    return Productos(**new_producto)

#ELIMINAR PRODUCTOS
@router.delete("/productos/{id}")
async def producto(id : str, user: UserDB = Depends(auth_user)):

    found = db_client.local.productos.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        raise HTTPException(status_code=400, detail="No hay usuarios con esa ID para eliminar.")
    
    return {"Bien" : "Se eliminó el prodcuto."}

# ACTUALIZAR PRODUCTOS
@router.put("/productos")
async def actualizar_producto(producto: Productos, user: UserDB = Depends(auth_user)):
    producto_dict = dict(producto)
    del producto_dict["id"]

    try:
        db_client.local.productos.find_one_and_replace(
            {"_id" : ObjectId(producto.id)}, producto_dict)
    except:
        return{"Error" : "No se encotró el producto"}
    return buscardb("_id", ObjectId(producto.id))
#BUSCAR POR ID
@router.get("/productos/{id}")
async def producto(id :str, user: UserDB = Depends(auth_user)):
    return buscardb("_id", ObjectId(id))

#BUSCAR POR NOMBRE
@router.get("/buscar")
async def producto(nombre :str, user: UserDB = Depends(auth_user)):
    return buscardb("nombre", nombre)

# BUSCAR PRODUCTOS POR CATEGORÍA
@router.get("/productos/categoria/{categoria}")
async def productos_por_categoria(categoria: str, user: UserDB = Depends(auth_user)):
    return buscardb_categoria("categoria", categoria)
    
# ORDENAR PRODUCTOS POR PRECIO
@router.get("/ordenar")
async def ordenar_productos(orden: str, user: UserDB = Depends(auth_user)):
    if orden == "ascendente":
        ordenados = db_client.local.productos.find().sort("precio", 1)
    elif orden =="descendente":
        ordenados = db_client.local.productos.find().sort("precio", -1)
    else:
        raise HTTPException(status_code=400, detail="El orden debe ser ascendente o descendente.")
    return productos_schema(ordenados)

# BORRAR PRODUCTOS POR CATEGORÍA
@router.delete("/productos/categoria/{categoria}/eliminar")
async def productos_por_categoria(categoria: str, user: UserDB = Depends(auth_user)):
    db_client.local.productos.delete_many({"categoria":categoria})
    return {"Bien" : f"Se eliminaron los productos de la categoria {categoria}"}
    
    
#FUNCIONES DE AYUDA
def buscardb(field : str, key):
    try:
        producto = db_client.local.productos.find_one({field : key})
        return Productos(**producto_schema(producto))
    except :
        return {"error": "No se encontraron productos."}
    
def buscardb_categoria(field : str, key):
    try:
        productos_buscar = db_client.local.productos.find({field: key})
        productos = [producto_schema(producto) for producto in productos_buscar]
        if productos:
            return productos
        else:
            return {"error": "No se encontraron productos de esa categoría."}
    except:
        return {"error": "No se encontraron productos de esa categoría."}
    