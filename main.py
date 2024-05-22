from fastapi import FastAPI
from routers import users, products

app = FastAPI()

#ROUTERS
app.include_router(users.router)
app.include_router(products.router)


@app.get("/")
async def saludo():
    return ("Desarrollado por Ismael Fernández Archilla.")