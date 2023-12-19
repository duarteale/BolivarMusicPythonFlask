from starlette.requests import Request
from fastapi import FastAPI, HTTPException
from routes.usuarios import user
from fastapi.middleware.cors import CORSMiddleware
from methods.cnx import SessionLocal
from models.models import *
from passlib.context import CryptContext

app = FastAPI()


# Origins admited
origins = ["*"]

# Add Middleware CORS (Cross-Origin Resource Sharing )
app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# Routes
app.include_router(user, prefix='/users')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(password_plana, password_hash):
    return pwd_context.verify(password_plana, password_hash)

@app.get('/')
def root():
    return 'Hola, todavía no funciona. Gracias por esperar :D'

@app.get('/test')
def test():
    resp = {'nombre':'Daniel', 'apellido': 'Cazabat', 'edad': 53} #Para el navegador es un JSON
    return resp