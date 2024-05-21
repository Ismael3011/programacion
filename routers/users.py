from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from db.client import db_client
from schemas.users import user_schema, users_schema


router = APIRouter()
ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 5
SECRET = "183c0ed4e2210e4c3ff66c0d0227ea362592cf2dfb4bb1e58f375b3ddfbef3c5"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    id : str | None
    username: str
    email: str

class UserDB(User):
    password: str

async def auth_user(token:str= Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    
    return search_user(username)

#async def current_user(user : UserDB = Depends (auth_user)):
#   return user

@router.get("/users")
async def user():
    return users_schema(db_client.local.users.find())

@router.post("/user")
async def user(user : UserDB):
    buscar = buscardb_user("email", user.email)
    if buscar:
        raise HTTPException(status_code=400, detail="Ya hay usuarios con ese email.")

    user_dict = user.dict()
    del user_dict["id"]

    id = db_client.local.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.local.users.find_one({"_id": id}))

    return UserDB(**new_user)

#Autenticación.
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user =  buscardb_user("username", form.username)
    if not user:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no encontrado.")

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta.")

    acces_token = {"sub":user.username, "exp":datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)}
    return {"access_token": jwt.encode(acces_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

#FUNCIONES DE AYUDA
def buscardb_user(field : str, key):
    user = db_client.local.users.find_one({field: key})
    if user:
        return UserDB(**user_schema(user))
    return None
    
def search_user(username: str):
    user = db_client.remote_db.users.find_one({"username": username})
    if user:
        return User(**user_schema(user))
    return None

def search_userdb(username: str):
    user = db_client.remote_db.users.find_one({"username": username})
    if user:
        return UserDB(**user_schema(user))
    return None