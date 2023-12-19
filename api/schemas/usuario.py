from pydantic import BaseModel
from uuid import uuid4

class User(BaseModel):
    id: str = str(uuid4())
    username: str
    fullname: str
    email: str    

class CreateUser(BaseModel):
    username: str
    fullname: str
    email: str
    password: str

class CreateUserOut(BaseModel):
    id: str = str(uuid4())
    username: str
    fullname: str
    email: str

class UpdateUser(BaseModel):
    username: str
    fullname: str
    email: str    

class Login(BaseModel):
    username: str
    password: str

#Crear la ruta, el metodo PUT/PATCH siempre en usuario.
class ChangePassword(BaseModel):
    username: str
    password: str
    newPassword: str