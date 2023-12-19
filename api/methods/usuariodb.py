from schemas.usuario import *
from models.models import UsuarioDB
from methods.cnx import SessionLocal
from uuid import uuid4

# Function to get all Users 
def getUsers(activo=True):
    try:
        db = SessionLocal()
        users = db.query(UsuarioDB).filter(UsuarioDB.activo == activo).all()
        if users:
            db.close()
            return users
        return None
    except Exception as e:
        raise e
    finally:
        db.close()

# Function to get one task
def getUsuarioDB(id: str):
    try:
        db = SessionLocal()
        user = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
        if user:
            db.close()
            return user
        return None
    except Exception as e:
        raise e                   
    
# Creation of "user" is used in the "POST" method
def createUsuarioDB(user: CreateUser):
    try:
        db = SessionLocal()
        new_user = UsuarioDB(
                        id=str(uuid4()),
                        username=user.username, 
                        fullname=user.fullname, 
                        email=user.email, 
                        password=user.password              
                        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close_all()

# Function to get update the "User" is used in "PUT" methods
def updateUsuarioDB(id: str, updated_user: UpdateUser):
    try:
        db = SessionLocal()
        user = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
        print(user)
        if user:
            user.username=updated_user.username
            user.fullname=updated_user.fullname
            user.email=updated_user.email
            db.commit()
            db.refresh(user)
            return user
        return None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Function to remove a "User" by their ID, mode logical
def deleteUsuarioDB(id: str):
    try:
        db = SessionLocal()
        user = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
        if user:
            user.activo = False
            db.commit()
            db.refresh(user)
        db.close()
        return user
    except Exception as e:
        raise e
    finally:
        db.close()


def getUserLoginDB(user:Login):
    try:
        db = SessionLocal()
        user = db.query(UsuarioDB).filter(UsuarioDB.password == user.password, UsuarioDB.user == user.user).first()
        if user:
            db.close()
            return user
        return None
    except Exception as e:
        raise e 

def changePasswordDB(user:ChangePassword):
    try:
        db = SessionLocal()
        user = db.query(UsuarioDB).filter(UsuarioDB.password == user.password, UsuarioDB.user == user.user).first()
        if user:
            user.password=user.newPassword
            db.commit()
            db.refresh(user)
            db.close()
            return user
        return None
    except Exception as e:
        raise e 