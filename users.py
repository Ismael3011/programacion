from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta, date, time
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext


app = FastAPI()
ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 1
SECRET = "183c0ed4e2210e4c3ff66c0d0227ea362592cf2dfb4bb1e58f375b3ddfbef3c5"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    email: str

class UserDB(User):
    password: str

users_db = {
    "ismael": {
        "username": "ismael",
        "email": "ismael@sasa.es",
        "password": "$2a$12$5XsD1CiLYCqlMjkK5uHahOfbtPskDNYubtkk1/y2R3jkBy6SFT83i", #123456
    },
    "paco": {
        "username": "paco",
        "email": "paco@sasa.es",
        "password": "$2a$12$QaMTm2lwfbyJrSUf.FKkqOy7RknwHlzigKlgyf6Pmlud6slKFJy3K", #654321
    }
}
@app.get("/users")
async def user():
    return users_db
@app.post("/registrarse")
async def producto(user : UserDB):
    if type (search_user(user.email)) == User:
        raise HTTPException(status_code=400, detail="Ya hay usuarios con ese mail.")
    else :
        users_db.append(user)
        return producto

def search_userdb(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token:str= Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    
    return search_user(username)

async def current_user(user: User= Depends(auth_user)):
    return user

#Autenticación.
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db =  users_db.get(form.username)
    if not user_db:
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no encontrado.")
    user = search_userdb(form.username)

    crypt.verify(form.password, user.password)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta.")

    acces_token = {"sub":user.username, "exp":datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION)}
    return {"access_token": jwt.encode(acces_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}